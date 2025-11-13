from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.schemas.ScriptSchemas import VideoStoryBoard

class ScriptEditRequest(BaseModel):
    script: VideoStoryBoard

class WorkflowStatusResponse(BaseModel):
    status: str
    message: str
    progress: int
    data: Optional[Dict[str, Any]] = None

class WorkflowStartResponse(BaseModel):
    workflow_id: str
    message: str
    script: VideoStoryBoard