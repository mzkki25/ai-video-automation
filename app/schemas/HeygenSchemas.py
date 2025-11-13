from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class HeygenReturn(BaseModel):
    heygen_video_1: Dict[str, Any] = Field(..., description="Heygen video 1")
    heygen_video_2: Dict[str, Any] = Field(..., description="Heygen video 2")
    heygen_video_3: Dict[str, Any] = Field(..., description="Heygen video 3")
    heygen_video_4: Dict[str, Any] = Field(..., description="Heygen video 4")
    
class HeygenStatus(BaseModel):
    video_status_1: Dict[str, Any] = Field(..., description="Heygen status 1")
    video_status_2: Dict[str, Any] = Field(..., description="Heygen status 2")
    video_status_3: Dict[str, Any] = Field(..., description="Heygen status 3")
    video_status_4: Dict[str, Any] = Field(..., description="Heygen status 4")