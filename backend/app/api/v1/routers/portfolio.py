from typing import Annotated

from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from backend.app.services.abc.abc_portfolio_service import BasePortfolioService
from app.core.security.abc import BaseJWTSecurity
from app.responses import (
     isresponse,
     router_responses,
     PortfolioSkinCreateSuccess,
     SkinDeleteSuccess,
     ServerError,
     OffsetError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     SkinNotExistsError,
     SkinPortfolioAlreadyExistsError,
     SkinNotFoundError
)
from app.schemas.dto import UserPortfolioDTO
from app.schemas import SkinsPage, PaginatePortfolioSkinsModel


user_portfolio_router = APIRouter(
     prefix="/api/v1/user",
     tags=["Portfolio"]
)



@user_portfolio_router.get(
     path="/skins", 
     response_model=SkinsPage[UserPortfolioDTO],
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
     token_payload: FromDishka[BaseJWTSecurity],
     paginate_data: Annotated[PaginatePortfolioSkinsModel, Form()]
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
     path="/skins",
     responses=router_responses(
          PortfolioSkinCreateSuccess,
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          SkinNotFoundError,
          SkinPortfolioAlreadyExistsError
     ),
     summary="Создание нового скина в портфолио."
)
async def create_skin_portfolio(
     uow: FromDishka[BaseUnitOfWork],
     service: FromDishka[BasePortfolioService],
     cache: FromDishka[Cache],
     token_payload: FromDishka[BaseJWTSecurity],
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
     path="/skins",
     responses=router_responses(
          SkinDeleteSuccess,
          ServerError,
          JWTTokenInvalidError,
          JWTTokenExpireError,
          SkinNotFoundError,
          SkinNotExistsError
     ),
     summary="Удаление скина из портфолио."
)
async def delete_skin_portfolio(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     token_payload: FromDishka[BaseJWTSecurity],
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