from fastapi import APIRouter
from app.utils.avatar_selection import get_all_avatars

router = APIRouter(prefix="/api/avatars", tags=["avatars"])

@router.get("")
def list_avatars():
    """Get list of available avatars"""
    return {"avatars": get_all_avatars()}
