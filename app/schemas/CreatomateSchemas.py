from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CreatoamateReturn(BaseModel):
    creatomate_video_1: Dict[str, Any] = Field(..., description="Creatomate video 1")
    creatomate_video_2: Dict[str, Any] = Field(..., description="Creatomate video 2")
    creatomate_video_3: Dict[str, Any] = Field(..., description="Creatomate video 3")
    creatomate_video_4: Dict[str, Any] = Field(..., description="Creatomate video 4")
    
class CreatomateStatus(BaseModel):
    creatomate_render_status_1: Dict[str, Any] = Field(..., description="Creatomate render status 1")
    creatomate_render_status_2: Dict[str, Any] = Field(..., description="Creatomate render status 2")
    creatomate_render_status_3: Dict[str, Any] = Field(..., description="Creatomate render status 3")
    creatomate_render_status_4: Dict[str, Any] = Field(..., description="Creatomate render status 4")