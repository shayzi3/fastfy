from typing import Annotated

from fastapi import APIRouter, Query
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.infrastracture.cache.abc import Cache
from app.services.abc import BaseSkinService
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses import (
     isresponse,
     router_responses,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     NotFoundError
)
from app.schemas.dto import SkinDTO
from app.schemas import (
     SkinHistoryTimePartModel, 
     SkinsPage, 
     PaginateSkinsModel,
     JWTTokenPayloadModel
)


skin_router = APIRouter(
     prefix="/api/v1",
     tags=["Skin"],
     route_class=DishkaRoute
)



@skin_router.get(
     path="/skin", 
     response_model=SkinDTO,
     responses=router_responses(
          NotFoundError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Получение данных скина."
)
async def get_skin(
     _: FromDishka[JWTTokenPayloadModel],
     service: FromDishka[BaseSkinService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     skin_name: str
):
     result = await service.get_skin(
          cache=cache,
          uow=uow,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result
     
     
          
@skin_router.get(
     path="/skin/search", 
     response_model=SkinsPage[SkinDTO],
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Поиск скинов."
)
async def search_skin(
     _: FromDishka[JWTTokenPayloadModel],
     service: FromDishka[BaseSkinService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     paginate_data: Annotated[PaginateSkinsModel, Query()]
):
     result = await service.search_skin(
          cache=cache,
          uow=uow,
          paginate_data=paginate_data,
     )
     if isresponse(result):
          return result.response()
     return result     
     
     
@skin_router.get(
     path="/skin/history", 
     response_model=SkinHistoryTimePartModel,
     responses=router_responses(
          NotFoundError,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Получение истории изменения цены скина."
)
async def skin_history(
     _: FromDishka[JWTTokenPayloadModel],
     service: FromDishka[BaseSkinService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     skin_name: str
):
     result = await service.skin_price_history(
          cache=cache,
          uow=uow,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result
