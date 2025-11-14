import uuid
import json
import logging
from fastapi import HTTPException, UploadFile, BackgroundTasks
from typing import Optional
from sqlalchemy.orm import Session

from app.controller.WorkflowProductController import WorkflowProductController
from app.service.WorkflowService import WorkflowService
from app.service.FileService import FileService
from app.schemas.InputSchemas import InputPayload, InputImage, ScriptReturn
from app.schemas.WorkflowSchemas import ScriptEditRequest, WorkflowStatusResponse, WorkflowStartResponse
from app.schemas.ScriptSchemas import VideoStoryBoard
from app.models.Video import Video
from app.models.User import User

logger = logging.getLogger(__name__)

class VideoController:
    def __init__(self, db: Optional[Session] = None, user: Optional[User] = None):
        self.workflow_service = WorkflowService(db, user.id if user else None)
        self.db = db
        self.user = user
    
    async def generate_script(
        self,
        nama_produk: str,
        target_audiens: str,
        usp: str,
        cta: str,
        product_image: UploadFile,
        talking_photo_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        avatar_image: Optional[UploadFile] = None,
        avatar_url: Optional[str] = None
    ) -> ScriptReturn:
        """Generate video script"""
        try:
            # Process uploaded files
            product_image_path, avatar_image_path = await FileService.process_uploaded_files(
                product_image, avatar_image
            )
            
            # Create request objects
            payload = InputPayload(
                nama_produk=nama_produk,
                target_audiens=target_audiens,
                usp=usp,
                cta=cta,
                talking_photo_id=talking_photo_id,
                voice_id=voice_id
            )
            
            image_request = InputImage(
                product_image=product_image_path,
                avatar_image=avatar_url if avatar_url else avatar_image_path
            )
            
            # Generate script
            controller = WorkflowProductController(payload, image_request)
            script_result = await controller.generate_video_script()
            
            # Cleanup temp files
            FileService.cleanup_temp_file(product_image_path)
            if avatar_image_path:
                FileService.cleanup_temp_file(avatar_image_path)
            
            return script_result
            
        except Exception as e:
            logger.error(f"Error generating script: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")
    
    async def generate_script_non_product(
        self,
        nama_produk: str,
        target_audiens: str,
        usp: str,
        cta: str,
        talking_photo_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        avatar_image: Optional[UploadFile] = None,
        avatar_url: Optional[str] = None
    ) -> ScriptReturn:
        """Generate video script for non-product video"""
        try:
            # Process avatar image only
            avatar_image_path = None
            if avatar_image and avatar_image.filename:
                avatar_image_path = await FileService.save_uploaded_file(avatar_image)
            
            # Create request objects
            payload = InputPayload(
                nama_produk=nama_produk,
                target_audiens=target_audiens,
                usp=usp,
                cta=cta,
                talking_photo_id=talking_photo_id,
                voice_id=voice_id
            )
            
            image_request = InputImage(
                product_image=None,
                avatar_image=avatar_url if avatar_url else avatar_image_path
            )
            
            # Generate script
            controller = WorkflowProductController(payload, image_request, is_non_product=True)
            script_result = await controller.generate_video_script()
            
            # Cleanup temp files
            if avatar_image_path:
                FileService.cleanup_temp_file(avatar_image_path)
            
            return script_result
            
        except Exception as e:
            logger.error(f"Error generating non-product script: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating script: {str(e)}")
    
    async def edit_script(self, request: ScriptEditRequest) -> dict:
        """Edit script"""
        try:
            return {
                "message": "Script berhasil diupdate",
                "script": request.script
            }
        except Exception as e:
            logger.error(f"Error editing script: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error editing script: {str(e)}")
    
    async def start_workflow(
        self,
        background_tasks: BackgroundTasks,
        nama_produk: str,
        target_audiens: str,
        usp: str,
        cta: str,
        product_image: UploadFile,
        talking_photo_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        avatar_image: Optional[UploadFile] = None,
        avatar_url: Optional[str] = None,
        script: Optional[str] = None
    ) -> WorkflowStartResponse:
        """Start workflow"""
        try:
            workflow_id = str(uuid.uuid4())
            
            # Save to database
            if self.db and self.user:
                video = Video(
                    user_id=self.user.id,
                    workflow_id=workflow_id,
                    nama_produk=nama_produk,
                    status="processing"
                )
                self.db.add(video)
                self.db.commit()
            
            # Process uploaded files
            product_image_path, avatar_image_path = await FileService.process_uploaded_files(
                product_image, avatar_image
            )
            
            # Create request objects
            payload = InputPayload(
                nama_produk=nama_produk,
                target_audiens=target_audiens,
                usp=usp,
                cta=cta,
                talking_photo_id=talking_photo_id,
                voice_id=voice_id
            )
            
            image_request = InputImage(
                product_image=product_image_path,
                avatar_image=avatar_url if avatar_url else avatar_image_path
            )
            
            controller = WorkflowProductController(payload, image_request)
            
            # Generate or use provided script
            if script:
                script_data = json.loads(script)
                script_result = ScriptReturn(
                    script=VideoStoryBoard(**script_data),
                    product_url=controller.product_url,
                    avatar_url=controller.avatar_url
                )
            else:
                self.workflow_service.update_status(workflow_id, "processing", "Generating script...", 5)
                script_result = await controller.generate_video_script()
            
            # Start background workflow
            background_tasks.add_task(
                self.workflow_service.run_workflow, 
                workflow_id, 
                controller, 
                script_result
            )
            
            return WorkflowStartResponse(
                workflow_id=workflow_id,
                message="Workflow started successfully",
                script=script_result.script
            )
            
        except Exception as e:
            logger.error(f"Error starting workflow: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error starting workflow: {str(e)}")
    
    async def start_workflow_non_product(
        self,
        background_tasks: BackgroundTasks,
        nama_produk: str,
        target_audiens: str,
        usp: str,
        cta: str,
        talking_photo_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        avatar_image: Optional[UploadFile] = None,
        avatar_url: Optional[str] = None,
        script: Optional[str] = None
    ) -> WorkflowStartResponse:
        """Start workflow for non-product video"""
        try:
            workflow_id = str(uuid.uuid4())
            
            # Save to database
            if self.db and self.user:
                video = Video(
                    user_id=self.user.id,
                    workflow_id=workflow_id,
                    nama_produk=nama_produk,
                    status="processing"
                )
                self.db.add(video)
                self.db.commit()
            
            # Process avatar image only
            avatar_image_path = None
            if avatar_image:
                avatar_image_path = await FileService.save_uploaded_file(avatar_image)
            
            # Create request objects
            payload = InputPayload(
                nama_produk=nama_produk,
                target_audiens=target_audiens,
                usp=usp,
                cta=cta,
                talking_photo_id=talking_photo_id,
                voice_id=voice_id
            )
            
            image_request = InputImage(
                product_image=None,
                avatar_image=avatar_url if avatar_url else avatar_image_path
            )
            
            controller = WorkflowProductController(payload, image_request, is_non_product=True)
            
            # Generate or use provided script
            if script:
                script_data = json.loads(script)
                script_result = ScriptReturn(
                    script=VideoStoryBoard(**script_data),
                    product_url="",
                    avatar_url=controller.avatar_url
                )
            else:
                self.workflow_service.update_status(workflow_id, "processing", "Generating script...", 5)
                script_result = await controller.generate_video_script()
            
            # Start background workflow
            background_tasks.add_task(
                self.workflow_service.run_workflow, 
                workflow_id, 
                controller, 
                script_result
            )
            
            return WorkflowStartResponse(
                workflow_id=workflow_id,
                message="Workflow started successfully",
                script=script_result.script
            )
            
        except Exception as e:
            logger.error(f"Error starting non-product workflow: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error starting non-product workflow: {str(e)}")
    
    def get_workflow_status(self, workflow_id: str) -> WorkflowStatusResponse:
        """Get workflow status"""
        status_data = self.workflow_service.get_status(workflow_id)
        
        if not status_data:
            logger.warning(f"Workflow status requested for unknown ID: {workflow_id}")
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        logger.info(f"Workflow {workflow_id}: Status check - {status_data['status']} - {status_data['message']}")
        
        return WorkflowStatusResponse(
            status=status_data['status'],
            message=status_data['message'],
            progress=status_data['progress'],
            data=status_data.get('data')
        )