from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VideoResponse(BaseModel):
    id: int
    workflow_id: str
    nama_produk: str
    status: str
    video_url: Optional[str]
    thumbnail_url: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VideoListResponse(BaseModel):
    total: int
    videos: List[VideoResponse]

class BulkDeleteRequest(BaseModel):
    ids: List[int]
    
    @property
    def video_ids(self):
        return self.ids
