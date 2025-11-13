from pydantic import BaseModel
from datetime import datetime
from typing import List

class TemplateCreate(BaseModel):
    name: str
    nama_produk: str
    target_audiens: str
    usp: str
    cta: str

class TemplateResponse(BaseModel):
    id: int
    name: str
    nama_produk: str
    target_audiens: str
    usp: str
    cta: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TemplateListResponse(BaseModel):
    templates: List[TemplateResponse]
