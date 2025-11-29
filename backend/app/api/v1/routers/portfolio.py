from typing import Annotated

from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.services.abc.abc_portfolio_service import BasePortfolioService
from app.responses import (
     isresponse,
     router_responses,
     ServerError,
     OffsetError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     CreateSuccess,
     DeleteSuccess,
     DataAlreadyExistsError,
     DataNotExistsError,
)
from app.schemas.dto import SkinPortfolioDTO
from app.schemas import SkinsPage, PaginateSkinsModel, JWTTokenPayloadModel


user_portfolio_router = APIRouter(
     prefix="/api/v1",
     tags=["Portfolio"],
     route_class=DishkaRoute
)



@user_portfolio_router.get(
     path="/portfolio", 
     response_model=SkinsPage[SkinPortfolioDTO],
     responses=router_responses(
          ServerError,
          OffsetError,
          JWTTokenInvalidError,
          JWTTokenExpireError
     ),
     summary="Получение скинов портфолио.",
     response_model_exclude={"user", "user_uuid"}
)
async def get_portfolio(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BasePortfolioService],
     token_payload: FromDishka[JWTTokenPayloadModel],
     paginate_data: Annotated[PaginateSkinsModel, Form()]
):
     result = await service.get_skins_portfolio(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          paginate_data=paginate_data
     )
     if isresponse(result):
          return result.response()
     return result
          
     
    
     
@user_portfolio_router.post(
     path="/portfolio",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          CreateSuccess,
          DataAlreadyExistsError
     ),
     summary="Создание нового скина в портфолио."
)
async def create_skin_portfolio(
     uow: FromDishka[BaseUnitOfWork],
     service: FromDishka[BasePortfolioService],
     cache: FromDishka[Cache],
     token_payload: FromDishka[JWTTokenPayloadModel],
     skin_name: str
):
     result = await service.create_skin_portfolio(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          skin_name=skin_name,
     )
     return result.response()

     
     
     
@user_portfolio_router.delete(
     path="/portfolio",
     responses=router_responses(
          ServerError,
          JWTTokenInvalidError,
          JWTTokenExpireError,
          DeleteSuccess,
          DataNotExistsError
     ),
     summary="Удаление скина из портфолио."
)
async def delete_skin_portfolio(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[JWTTokenPayloadModel],
     service: FromDishka[BasePortfolioService],
     skin_name: str
):
     result = await service.delete_skin_portolio(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          skin_name=skin_name
     )
     return result.response()