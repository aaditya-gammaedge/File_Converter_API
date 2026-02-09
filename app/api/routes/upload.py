from fastapi import APIRouter, Depends
from app.api.auth.dependencies import get_current_user
from app.db.models import User

router = APIRouter()

@router.post("/upload")
async def upload_file(
    current_user: User = Depends(get_current_user)
):
    return {"user_id": current_user.id}







