from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.session import AsyncSession, get_async_session
from app.infrastracture.redis import RedisPool, get_redis_session
from app.responses import isresponse
from app.schemas import TokenPayload, UserModel, SteamItem
from ..dependency import current_user
from .service import UserService, get_user_service



user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"]
)



@user_router.get(path="/user")
async def get_user(
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserService, Depends(get_user_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     uuid: str | None = None
) -> UserModel:
     user = current_user.uuid if uuid is None else uuid
     result = await service.get_user(
          async_session=async_session,
          redis_session=redis_session,
          uuid=user
     )
     if isresponse(result):
          return result.response()
     return result
     
     
     
@user_router.get(path="/user/SteamInventory")
async def get_steam_inventory(
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserService, Depends(get_user_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     uuid: str | None = None
) -> list[SteamItem]:
     user = current_user.uuid if uuid is None else uuid
     result = await service.get_user_steam_inventory(
          async_session=async_session,
          redis_session=redis_session,
          uuid=user
     )
     
     if isresponse(result):
          return result.response()
     return result