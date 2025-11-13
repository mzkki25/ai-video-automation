from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import Optional
from datetime import datetime
from app.core.Database import get_db
from app.models.User import User
from app.models.Video import Video
from app.schemas.VideoSchemas import VideoListResponse, VideoResponse, BulkDeleteRequest
from app.middleware.AuthMiddleware import get_current_user

router = APIRouter(prefix="/api", tags=["history"])

@router.get("/videos")
def get_videos(
    search: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Video).filter(Video.user_id == current_user.id)
    
    if search:
        query = query.filter(Video.nama_produk.ilike(f"%{search}%"))
    
    if status:
        query = query.filter(Video.status == status)
    
    videos = query.order_by(desc(Video.created_at)).offset(skip).limit(limit).all()
    
    return [{
        "id": str(v.id),
        "title": v.nama_produk,
        "thumbnail": v.thumbnail_url,
        "status": v.status,
        "created_at": v.created_at.isoformat() if v.created_at else None,
        "workflow_id": v.workflow_id,
        "product_name": v.nama_produk,
        "video_url": v.video_url
    } for v in videos]

@router.delete("/videos")
def delete_videos(
    request: BulkDeleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted = db.query(Video).filter(
        Video.id.in_(request.video_ids),
        Video.user_id == current_user.id
    ).delete(synchronize_session=False)
    
    db.commit()
    
    return {"deleted": deleted}

@router.get("/videos/{video_id}", response_model=VideoResponse)
def get_video_detail(
    video_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    video = db.query(Video).filter(
        Video.id == video_id,
        Video.user_id == current_user.id
    ).first()
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return video
