from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks, Query

from app.responses import (
     isresponse,
     router_responses,
     PortfolioSkinCreateSuccess,
     SkinPortfolioAlreadyExists,
     PortfolioEmpty,
     SkinNotExists,
     SkinDeleteSuccess,
     AuthError,
     SecretTokenError,
     ServerError,
     OffsetError
)
from app.db.session import get_async_session, AsyncSession
from app.infrastracture.redis import get_redis_session, RedisPool
from app.schemas import UserSkinRelModel, SkinsPage
from .service import get_user_portfolio_service, UserPortfolioService
from ..dependency import valide_secret_bot_token, current_user_uuid



user_portfolio_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User", "User Portfolio", "Bot"],
     dependencies=[Depends(valide_secret_bot_token)]
)



@user_portfolio_router.get(
     path="/portfolio", 
     response_model=SkinsPage[UserSkinRelModel],
     responses=router_responses(
          PortfolioEmpty,
          AuthError,
          ServerError,
          SecretTokenError,
          OffsetError
     ),
     summary="Получение портфолио текущего аккаунта.",
     response_model_exclude={"user"}
)
async def get_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     service: Annotated[UserPortfolioService,Depends(get_user_portfolio_service)],
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     offset: int = Query(ge=0),
     limit: int = Query(ge=1, le=50)
):
     result = await service.get_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user_uuid,
          offset=offset,
          limit=limit
     )
     if isresponse(result):
          return result.response()
     return result
          
     
    
     
@user_portfolio_router.post(
     path="/portfolio",
     responses=router_responses(
          SkinPortfolioAlreadyExists,
          PortfolioSkinCreateSuccess,
          AuthError,
          ServerError,
          SecretTokenError
     ),
     summary="Создание нового предмета в портфолио текущего аккаунта."
)
async def post_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     background_tasks: BackgroundTasks,
     skin_name: str
):
     result = await service.post_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          skin_name=skin_name,
          user_uuid=current_user_uuid
     )
     background_tasks.add_task(
          func=service._after_post_portfolio,
          async_session=async_session,
          skin_name=skin_name
     )
     return result.response()

     
     
     
@user_portfolio_router.delete(
     path="/portfolio",
     responses=router_responses(
          SkinNotExists,
          SkinDeleteSuccess,
          AuthError,
          ServerError,
          SecretTokenError
     ),
     summary="Удаление скина из портфолио текущего аккаунта."
)
async def delete_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     current_user_uuid: Annotated[str, Depends(current_user_uuid)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     skin_name: str
):   
     result = await service.delete_portfolio(
          async_session=async_session,
          user_uuid=current_user_uuid,
          skin_name=skin_name
     )
     return result.response()