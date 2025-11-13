from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.ScriptSchemas import VideoStoryBoard

class InputPayload(BaseModel):
    nama_produk: str = Field(..., description="Nama produk")
    target_audiens: str = Field(..., description="Target audiens")
    usp: str = Field(..., description="Unique selling point")
    cta: str = Field(..., description="Call to action")
    talking_photo_id: Optional[str] = Field(default=None, description="Talking photo id")
    voice_id: Optional[str] = Field(default=None, description="Voice id")
    
class ScriptReturn(BaseModel):
    script: VideoStoryBoard = Field(..., description="Video script")
    product_url: str = Field(..., description="Product image")
    avatar_url: str = Field(..., description="Avatar image")

class InputImage(BaseModel):
    product_image: Optional[str] = Field(..., description="Product image")
    avatar_image: Optional[str] = Field(..., description="Avatar image")