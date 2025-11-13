from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.User import User
from app.middleware.AuthMiddleware import get_current_user
from app.service.FileService import FileService
import os

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Only image files allowed")
    
    if file.size and file.size > 3 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 3MB")
    
    file_service = FileService()
    file_url = await file_service.upload_file(file, f"user_{current_user.id}")
    
    return {"url": file_url}
