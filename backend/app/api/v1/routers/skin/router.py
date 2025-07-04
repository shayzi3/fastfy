from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from app.api.v1.routers.dependency import current_user
from app.infrastracture.redis import RedisPool
from app.responses import ArgumentError, isresponse
from app.schemas import SkinModel, SkinHistoryTimePartModel
from ..dependency import current_user, get_async_session, get_redis_session
from .service import SkinService, get_skin_service


skin_router = APIRouter(
     prefix="/api/v1",
     tags=["Skin"],
     dependencies=[Depends(current_user)]
)



@skin_router.get("/skin", response_model=SkinModel)
async def get_skin(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     skin_id: str | None = None,
     skin_name: str | None = None
):
     if (skin_id is None) and (skin_name is None):
          return ArgumentError.response()
     
     result = await service.get_skin(
          async_session=async_session,
          redis_session=redis_session,
          skin_id=skin_id,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result
     
     
          
     
@skin_router.get("/skin/search", response_model=list[SkinModel])
async def search_skin(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     query: str,
     steam: bool,
     offset: int = 0
):
     result = await service.search_skin(
          async_session=async_session,
          redis_session=redis_session,
          query=query,
          steam=steam,
          offset=offset
     )
     if isresponse(result):
          return result.response()
     return result
     
     
     
@skin_router.get("/skin/history", response_model=SkinHistoryTimePartModel)
async def skin_history(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     skin_id: str | None = None,
     skin_name: str | None = None
):
     if (skin_id is None) and (skin_name is None):
          return ArgumentError.response()
          
     result = await service.skin_history(
          async_session=async_session,
          redis_session=redis_session,
          skin_id=skin_id,
          skin_name=skin_name
     )
     return result
