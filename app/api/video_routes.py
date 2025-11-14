from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.controller.VideoController import VideoController
from app.schemas.InputSchemas import ScriptReturn
from app.schemas.WorkflowSchemas import ScriptEditRequest, WorkflowStatusResponse, WorkflowStartResponse
from app.service.HeygenService import HeygenService
from app.service.CreatomateGenerator import CreatomateGenerator
from app.core.Database import get_db
from app.models.User import User
from app.middleware.AuthMiddleware import get_current_user

router = APIRouter(prefix="/api/video", tags=["video"])

@router.post("/generate-script")
async def generate_script(
    nama_produk: str = Form(...),
    target_audiens: str = Form(...),
    usp: str = Form(...),
    cta: str = Form(...),
    talking_photo_id: Optional[str] = Form(None),
    voice_id: Optional[str] = Form(None),
    product_image: UploadFile = File(...),
    avatar_image: Optional[UploadFile] = File(None),
    avatar_url: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate video script berdasarkan input pengguna"""
    video_controller = VideoController(db, current_user)
    result = await video_controller.generate_script(
        nama_produk, target_audiens, usp, cta, product_image,
        talking_photo_id, voice_id, avatar_image, avatar_url
    )
    
    # Flatten response to match frontend expectations
    return {
        "title": result.script.title,
        "script": result.script.script,
        "scripts": [s.model_dump() for s in result.script.scripts],
        "product_url": result.product_url,
        "avatar_url": result.avatar_url
    }

@router.post("/generate-script-non-product")
async def generate_script_non_product(
    nama_produk: str = Form(...),
    target_audiens: str = Form(...),
    usp: str = Form(...),
    cta: str = Form(...),
    talking_photo_id: Optional[str] = Form(None),
    voice_id: Optional[str] = Form(None),
    avatar_image: Optional[UploadFile] = File(None),
    avatar_url: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate video script for non-product video"""
    video_controller = VideoController(db, current_user)
    result = await video_controller.generate_script_non_product(
        nama_produk, target_audiens, usp, cta,
        talking_photo_id, voice_id, avatar_image, avatar_url
    )
    
    return {
        "title": result.script.title,
        "script": result.script.script,
        "scripts": [s.model_dump() for s in result.script.scripts],
        "product_url": result.product_url,
        "avatar_url": result.avatar_url
    }

@router.put("/edit-script")
async def edit_script(
    request: ScriptEditRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Edit script yang sudah dibuat"""
    video_controller = VideoController(db, current_user)
    return await video_controller.edit_script(request)

@router.post("/start-workflow", response_model=WorkflowStartResponse)
async def start_workflow(
    background_tasks: BackgroundTasks,
    nama_produk: str = Form(...),
    target_audiens: str = Form(...),
    usp: str = Form(...),
    cta: str = Form(...),
    talking_photo_id: Optional[str] = Form(None),
    voice_id: Optional[str] = Form(None),
    product_image: UploadFile = File(...),
    avatar_image: Optional[UploadFile] = File(None),
    avatar_url: Optional[str] = Form(None),
    script: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start workflow lengkap secara asynchronous"""
    video_controller = VideoController(db, current_user)
    return await video_controller.start_workflow(
        background_tasks, nama_produk, target_audiens, usp, cta, product_image,
        talking_photo_id, voice_id, avatar_image, avatar_url, script
    )

@router.post("/start-workflow-non-product", response_model=WorkflowStartResponse)
async def start_workflow_non_product(
    background_tasks: BackgroundTasks,
    nama_produk: str = Form(...),
    target_audiens: str = Form(...),
    usp: str = Form(...),
    cta: str = Form(...),
    talking_photo_id: Optional[str] = Form(None),
    voice_id: Optional[str] = Form(None),
    avatar_image: Optional[UploadFile] = File(None),
    avatar_url: Optional[str] = Form(None),
    script: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start workflow untuk non-product video (tanpa upload produk)"""
    video_controller = VideoController(db, current_user)
    return await video_controller.start_workflow_non_product(
        background_tasks, nama_produk, target_audiens, usp, cta,
        talking_photo_id, voice_id, avatar_image, avatar_url, script
    )

@router.get("/workflow-status/{workflow_id}", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get status workflow"""
    video_controller = VideoController(db, current_user)
    return video_controller.get_workflow_status(workflow_id)

@router.get("/heygen-status/{video_id}")
async def get_heygen_status(video_id: str):
    """Check status video Heygen"""
    try:
        heygen_service = HeygenService()
        status = await heygen_service.get_heygen_video_status(video_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting Heygen status: {str(e)}")

@router.get("/creatomate-status/{render_id}")
async def get_creatomate_status(render_id: str):
    """Check status render Creatomate"""
    try:
        creatomate_service = CreatomateGenerator()
        status = await creatomate_service.get_creatomate_render_status(render_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting Creatomate status: {str(e)}")