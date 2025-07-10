from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import UUID4

from app.responses import (
     isresponse,
     router_responses,
     PortfolioSkinSoonCreate,
     ArgumentError,
     PortfolioSkinCreateSuccess,
     SkinPortfolioAlreadyExists,
     PortfolioEmpty,
     SkinNotFoundError,
     SkinChangeSuccess,
     SkinNotExists,
     SkinDeleteSuccess,
     TokenError,
     HttpError
)
from app.db.session import get_async_session, AsyncSession
from app.infrastracture.redis import get_redis_session, RedisPool
from app.api.v1.routers.dependency import current_user
from app.schemas import TokenPayload, UserPortfolioRelModel
from .schema import CreateUpdateSkin
from .service import get_user_portfolio_service, UserPortfolioService



user_portfolio_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User", "User Portfolio"]
)



@user_portfolio_router.get(
     path="/portfolio", 
     response_model=list[UserPortfolioRelModel],
     responses=router_responses(
          TokenError,
          PortfolioEmpty
     )
)
async def get_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService,Depends(get_user_portfolio_service)],
     uuid: UUID4 | None = None
):
     result = await service.get_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid if uuid is None else uuid,
     )
     if isresponse(result):
          return result.response()
     return result
          
     
     
@user_portfolio_router.post(
     path="/portfolio",
     responses=router_responses(
          TokenError,
          SkinPortfolioAlreadyExists,
          PortfolioSkinCreateSuccess,
          PortfolioSkinSoonCreate,
          HttpError,
          SkinNotFoundError
     )
)
async def post_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     background_task: BackgroundTasks,
     skin_data: CreateUpdateSkin,
     skin_name: str
):
     result = await service.post_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid,
          skin_data=skin_data,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     
     background_task.add_task(
          service._post_portfolio_create_skin,
          async_session=async_session,
          redis_session=redis_session,
          skin=result,
          skin_data=skin_data,
          user_uuid=current_user.uuid
     )
     return PortfolioSkinSoonCreate.response()
     
     
     
     
@user_portfolio_router.patch(
     path="/portfolio",
     responses=router_responses(
          TokenError,
          SkinNotFoundError,
          SkinChangeSuccess
     )
)
async def patch_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     skin_data: CreateUpdateSkin,
     skin_name: str | None = None,
     item_id: UUID4 | None = None
):
     if (skin_name is None) and (item_id is None):
          return ArgumentError.response()
     
     if not skin_data.non_nullable():
          return ArgumentError.response()
     
     result = await service.patch_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid,
          skin_data=skin_data,
          skin_name=skin_name,
          item_id=item_id
     )
     return result.response()
     
     
     
@user_portfolio_router.delete(
     path="/portfolio",
     responses=router_responses(
          TokenError,
          SkinNotExists,
          SkinDeleteSuccess
     )
)
async def delete_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     skin_name: str | None = None,
     item_id: UUID4 | None = None
):
     if (skin_name is None) and (item_id is None):
          return ArgumentError.response()   
     
     result = await service.delete_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid,
          skin_name=skin_name,
          item_id=item_id
     )
     return result.response()