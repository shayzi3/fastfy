from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Query, Form, Depends
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.infrastracture.cache.abc import Cache
from app.services.abc import BaseUserService
from app.core.security.abc import JWTTokenPayloadModel
from app.repositories.abc_uow import BaseUnitOfWork
from app.api.v1.dependency.rate_limit import RateLimitDepend
from app.responses import (
     isresponse,
     router_responses,
     HttpError,
     SteamInventoryBlockedError,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     NotFoundError,
     UpdateSuccess,
     UpdateError,
     TooManyRequestError
)
from app.schemas.dto import UserDTO
from app.schemas import (
     SkinsPage, 
     SteamInventorySkinModel, 
     PatchUserModel, 
     JWTTokenPayloadModel
)




user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"],
     route_class=DishkaRoute
)



@user_router.get(
     path="/user", 
     response_model=UserDTO,
     responses=router_responses(
          NotFoundError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          TooManyRequestError
     ),
     summary="Получения данных текущего аккаунта.",
     dependencies=[Depends(RateLimitDepend(2, timedelta(seconds=10), "get_user"))]
)
async def get_user(
     service: FromDishka[BaseUserService],
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[JWTTokenPayloadModel]
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
          UpdateSuccess,
          UpdateError,
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
     token_payload: FromDishka[JWTTokenPayloadModel],
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
     cache: FromDishka[Cache],
     token_payload: FromDishka[JWTTokenPayloadModel],
     offset: int = Query(ge=0),
     limit: int = Query(ge=1, le=20)
):
     result = await service.get_user_steam_inventory(
          cache=cache,
          token_payload=token_payload,
          offset=offset,
          limit=limit
     )
     if isresponse(result):
          return result.response()
     return result