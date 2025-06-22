from typing import Annotated
from fastapi import APIRouter, Depends

from app.schemas import UserModel
from ..dependency import current_user
from .service import UserService, get_user_service


user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"]
)



@user_router.get(path="/user")
async def get_user(
     current_user: Annotated[UserModel, Depends(current_user)],
     service: Annotated[UserService, Depends(get_user_service)],
     uuid: str | None = None
):
     user = current_user.uuid if uuid is None else uuid
     result = await service