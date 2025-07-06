from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks

from app.db.session import get_async_session, AsyncSession
from app.infrastracture.redis import get_redis_session, RedisPool
from app.api.v1.routers.dependency import current_user
from app.schemas import TokenPayload, UserPortfolioRelModel
from app.responses import ArgumentError, isresponse, PortfolioSkinSoonCreate
from .schema import CreateUpdateSkin
from .service import get_user_portfolio_service, UserPortfolioService



user_portfolio_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User"]
)



@user_portfolio_router.get("/portfolio")
async def get_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService,Depends(get_user_portfolio_service)]
) -> list[UserPortfolioRelModel]:
     result = await service.get_portfolio(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid,
     )
     if isresponse(result):
          return result.response()
     return result
          
     
@user_portfolio_router.post("/portfolio")
async def post_portfolio(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserPortfolioService, Depends(get_user_portfolio_service)],
     background_task: BackgroundTasks,
     skin_data: CreateUpdateSkin,
     skin_name: str
):
     if not skin_data.non_nullable:
          return ArgumentError.response()
     
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
     
     
     
     
@user_portfolio_router.patch("/portfolio")
async def patch_portfolio():
     ...
     
     
@user_portfolio_router.delete("/portfolio")
async def delete_portfolio():
     ...