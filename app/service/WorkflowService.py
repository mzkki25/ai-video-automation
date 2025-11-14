import asyncio
import logging
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.controller.WorkflowProductController import WorkflowProductController
from app.schemas.InputSchemas import ScriptReturn
from app.models.Video import Video
from app.core.WorkflowStorage import workflow_storage

logger = logging.getLogger(__name__)

class WorkflowService:
    def __init__(self, db: Optional[Session] = None, user_id: Optional[int] = None):
        self.db = db
        self.user_id = user_id
    
    def update_status(self, workflow_id: str, status: str, message: str, progress: int, data: Dict = None):
        """Update workflow status"""
        workflow_storage.set(workflow_id, {
            "status": status,
            "message": message,
            "progress": progress,
            "data": data
        })
    
    def get_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status"""
        return workflow_storage.get(workflow_id)
    
    async def run_workflow(self, workflow_id: str, controller: WorkflowProductController, script_result: ScriptReturn):
        """Execute complete workflow"""
        try:
            print(f"\n{'='*60}")
            print(f"WORKFLOW START: {workflow_id}")
            print(f"{'='*60}")
            logger.info(f"Starting workflow {workflow_id}")
            self.update_status(workflow_id, "processing", "Generating Heygen videos...", 10)
            
            # STEP 2: Generate and wait for Heygen videos
            print(f"\n[STEP 2] Generating HeyGen videos...")
            heygen_videos = await controller.generate_heygen_video_title(script_result)
            print(f"[STEP 2] HeyGen videos initiated, waiting for completion...")
            heygen_status = await self._wait_for_heygen_completion(workflow_id, controller, heygen_videos)
            if not heygen_status:
                print(f"[STEP 2] ❌ HeyGen videos failed or timeout")
                return
            print(f"[STEP 2] ✅ All HeyGen videos completed")
            
            # STEP 3: Generate background images
            print(f"\n[STEP 3] Generating background images...")
            self.update_status(workflow_id, "processing", "Generating background images...", 50)
            logger.info(f"Workflow {workflow_id}: Generating background images")
            generated_images = await controller.generate_image(script_result, controller.product_url, controller.avatar_url)
            print(f"[STEP 3] ✅ All background images generated")
            
            # STEP 4: Generate and wait for Creatomate videos
            print(f"\n[STEP 4] Rendering with Creatomate...")
            self.update_status(workflow_id, "processing", "Rendering videos with Creatomate...", 60)
            creatomate_videos = await controller.creatomate_render_video_title(script_result, heygen_status, generated_images)
            print(f"[STEP 4] Creatomate renders initiated, waiting for completion...")
            creatomate_status = await self._wait_for_creatomate_completion(workflow_id, controller, creatomate_videos)
            if not creatomate_status:
                print(f"[STEP 4] ❌ Creatomate renders failed or timeout")
                return
            print(f"[STEP 4] ✅ All Creatomate renders completed")
            
            # STEP 5: Merge videos
            print(f"\n[STEP 5] Merging final video...")
            self.update_status(workflow_id, "processing", "Merging final video...", 95)
            logger.info(f"Workflow {workflow_id}: Merging final video")
            final_video_url = await controller.video_merging(creatomate_status)
            print(f"[STEP 5] ✅ Video merged successfully")
            
            # Complete
            print(f"\n{'='*60}")
            print(f"✅ WORKFLOW COMPLETED: {workflow_id}")
            print(f"Final video URL: {final_video_url}")
            print(f"{'='*60}\n")
            logger.info(f"Workflow {workflow_id}: Completed successfully - {final_video_url}")
            self.update_status(workflow_id, "completed", "Video berhasil dibuat", 100, {
                "final_video_url": final_video_url,
                "script": script_result.script.model_dump(),
                "heygen_videos": heygen_videos.model_dump(),
                "generated_images": generated_images.model_dump(),
                "creatomate_videos": creatomate_videos.model_dump()
            })
            
            # Update database
            if self.db and self.user_id:
                video = self.db.query(Video).filter(Video.workflow_id == workflow_id).first()
                if video:
                    video.status = "completed"
                    video.video_url = final_video_url
                    video.completed_at = datetime.utcnow()
                    self.db.commit()
            
            # Cleanup temporary files
            self._cleanup_temp_files()
            
        except Exception as e:
            print(f"\n{'='*60}")
            print(f"❌ WORKFLOW FAILED: {workflow_id}")
            print(f"Error: {str(e)}")
            print(f"{'='*60}\n")
            logger.error(f"Workflow {workflow_id}: Error - {str(e)}")
            import traceback
            traceback.print_exc()
            self.update_status(workflow_id, "error", f"Error: {str(e)}", 0)
            # Cleanup temporary files even on error
            self._cleanup_temp_files()
    
    async def _wait_for_heygen_completion(self, workflow_id: str, controller: WorkflowProductController, heygen_videos):
        """Wait for Heygen videos to complete"""
        max_attempts = 300
        attempt = 0
        
        self.update_status(workflow_id, "processing", "Waiting for Heygen videos to complete...", 20)
        
        while attempt < max_attempts:
            heygen_status = await controller.get_heygen_video_status(heygen_videos)
            
            logger.info(f"Workflow {workflow_id}: Attempt {attempt+1} - Heygen Status:")
            logger.info(f"Video 1: {heygen_status.video_status_1['data']['status']}")
            logger.info(f"Video 2: {heygen_status.video_status_2['data']['status']}")
            logger.info(f"Video 3: {heygen_status.video_status_3['data']['status']}")
            logger.info(f"Video 4: {heygen_status.video_status_4['data']['status']}")
            
            all_completed = all([
                status['data']['status'] == 'completed' 
                for status in [
                    heygen_status.video_status_1, 
                    heygen_status.video_status_2, 
                    heygen_status.video_status_3, 
                    heygen_status.video_status_4
                ]
            ])
            
            if all_completed:
                logger.info(f"Workflow {workflow_id}: All Heygen videos completed")
                return heygen_status
                
            attempt += 1
            progress = int(20 + (attempt * 20 / max_attempts))
            self.update_status(workflow_id, "processing", f"Waiting for Heygen videos... ({attempt}/{max_attempts})", progress)
            await asyncio.sleep(15)
        
        logger.error(f"Workflow {workflow_id}: Timeout waiting for Heygen videos")
        self.update_status(workflow_id, "error", "Timeout waiting for Heygen videos", 0)
        return None
    
    async def _wait_for_creatomate_completion(self, workflow_id: str, controller: WorkflowProductController, creatomate_videos):
        """Wait for Creatomate videos to complete"""
        max_attempts = 300
        attempt = 0
        
        self.update_status(workflow_id, "processing", "Waiting for Creatomate videos to complete...", 70)
        
        while attempt < max_attempts:
            creatomate_status = await controller.get_creatomate_render_status(creatomate_videos)
            
            logger.info(f"Workflow {workflow_id}: Attempt {attempt+1} - Creatomate Status:")
            logger.info(f"Render 1: {creatomate_status.creatomate_render_status_1['status']}")
            logger.info(f"Render 2: {creatomate_status.creatomate_render_status_2['status']}")
            logger.info(f"Render 3: {creatomate_status.creatomate_render_status_3['status']}")
            logger.info(f"Render 4: {creatomate_status.creatomate_render_status_4['status']}")
            
            all_succeeded = all([
                status['status'] == 'succeeded' 
                for status in [
                    creatomate_status.creatomate_render_status_1, 
                    creatomate_status.creatomate_render_status_2,
                    creatomate_status.creatomate_render_status_3, 
                    creatomate_status.creatomate_render_status_4
                ]
            ])
            
            if all_succeeded:
                logger.info(f"Workflow {workflow_id}: All Creatomate videos completed")
                return creatomate_status
                
            attempt += 1
            progress = int(70 + (attempt * 20 / max_attempts))
            self.update_status(workflow_id, "processing", f"Waiting for Creatomate videos... ({attempt}/{max_attempts})", progress)
            await asyncio.sleep(15)
        
        logger.error(f"Workflow {workflow_id}: Timeout waiting for Creatomate videos")
        self.update_status(workflow_id, "error", "Timeout waiting for Creatomate videos", 0)
        return None
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        import os
        import glob
        
        try:
            # Clean up temp image files
            temp_files = glob.glob("temp_*")
            for file in temp_files:
                try:
                    os.remove(file)
                    logger.info(f"Cleaned up temp file: {file}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup {file}: {e}")
            
            # Clean up gabungan video files
            gabungan_files = glob.glob("gabungan_*.mp4")
            for file in gabungan_files:
                try:
                    os.remove(file)
                    logger.info(f"Cleaned up gabungan file: {file}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup {file}: {e}")
                    
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")