from typing import Annotated

from fastapi import APIRouter, Query, Form
from dishka.integrations.fastapi import FromDishka

from app.infrastracture.cache.abc import Cache
from app.services.abc import BaseUserService
from app.core.security.abc import BaseJWTSecurity
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses import (
     isresponse,
     router_responses,
     UserNotFoundError,
     UserUpdateSuccess,
     HttpError,
     SteamInventoryBlockedError,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     UserUpdateError
)
from app.schemas import SkinsPage, SteamInventorySkinModel, PatchUserModel
from app.schemas.dto import UserDTO



user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"],
)



@user_router.get(
     path="/user", 
     response_model=UserDTO,
     responses=router_responses(
          UserNotFoundError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Получения данных текущего аккаунта."
)
async def get_user(
     service: FromDishka[BaseUserService],
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[BaseJWTSecurity]
):
     result = await service.get_user(
          cache=cache,
          uow=uow,
          token_payload=token_payload
     )
     if isresponse(result):
          return result.response()
     return result



@user_router.patch(
     path="/user",
     responses=router_responses(
          UserUpdateSuccess,
          UserUpdateError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Изменение данных у пользователя."
)
async def patch_user(
     service: FromDishka[BaseUserService],
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[BaseJWTSecurity],
     data: Annotated[PatchUserModel, Form()]
):
     result = await service.patch_user(
          cache=cache,
          uow=uow,
          data=data,
          token_payload=token_payload
     )
     return result.response()
     
     
     
@user_router.get(
     path="/user/SteamInventory", 
     response_model=SkinsPage[SteamInventorySkinModel],
     responses=router_responses(
          HttpError,
          SteamInventoryBlockedError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Получение Steam инвентаря текущего аккаунта."
)
async def get_steam_inventory(
     service: FromDishka[BaseUserService],
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[BaseJWTSecurity],
     offset: int = Query(ge=0),
     limit: int = Query(ge=1, le=20)
):
     result = await service.get_user_steam_inventory(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          offset=offset,
          limit=limit
     )
     if isresponse(result):
          return result.response()
     return result