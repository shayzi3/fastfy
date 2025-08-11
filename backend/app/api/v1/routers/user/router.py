from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.responses import (
     isresponse,
     router_responses,
     UserNotFoundError,
     UserUpdateSuccess,
     HttpError,
     SteamInventoryBlocked,
     AuthError,
     SecretTokenError,
     ServerError
)
from app.db.session import AsyncSession, get_async_session
from app.infrastracture.redis import RedisPool, get_redis_session
from app.schemas import UserModel, SkinsPage
from ..dependency import current_user_uuid, valide_secret_bot_token
from .service import UserService, get_user_service



user_router = APIRouter(
     prefix="/api/v1",
     tags=["User", "Bot"],
     dependencies=[Depends(valide_secret_bot_token)]
)



@user_router.get(
     path="/user", 
     response_model=UserModel,
     responses=router_responses(
          UserNotFoundError,
          AuthError,
          SecretTokenError,
          ServerError
     ),
     summary="Получения данных текущего аккаунта."
)
async def get_user(
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     service: Annotated[UserService, Depends(get_user_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
):
     result = await service.get_user(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user_uuid
     )
     if isresponse(result):
          return result.response()
     return result



@user_router.patch(
     path="/user",
     responses=router_responses(
          UserNotFoundError,
          UserUpdateSuccess,
          SecretTokenError,
          AuthError,
          ServerError
     ),
     summary="Изменение процента у текущего аккаунта."
)
async def patch_skin_percent_user(
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     service: Annotated[UserService, Depends(get_user_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     skin_percent: int = Query(ge=0, le=100),
):
     result = await service.patch_skin_percent_user(
          async_session=async_session,
          skin_percent=skin_percent,
          user_uuid=current_user_uuid
     )
     return result.response()
     
     
     
@user_router.get(
     path="/user/SteamInventory", 
     response_model=SkinsPage,
     response_model_exclude={"skin_model_obj"},
     responses=router_responses(
          HttpError,
          SteamInventoryBlocked,
          UserNotFoundError,
          SecretTokenError,
          AuthError,
          ServerError
     ),
     summary="Получение Steam инвентаря текущего аккаунта."
)
async def get_steam_inventory(
     service: Annotated[UserService, Depends(get_user_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     offset: int = Query(ge=0)
):
     result = await service.get_user_steam_inventory(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user_uuid,
          offset=offset
     )
     if isresponse(result):
          return result.response()
     return result