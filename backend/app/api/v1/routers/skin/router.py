from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.responses import (
     isresponse,
     router_responses,
     SkinNotFoundError,
     OffsetError,
     AuthError,
     SecretTokenError,
     ServerError
)
from app.db.session import get_async_session, AsyncSession
from app.infrastracture.redis import RedisPool, get_redis_session
from app.schemas import SkinModel, SkinHistoryTimePartModel, SkinsPage
from ..dependency import valide_secret_bot_token
from .service import SkinService, get_skin_service


skin_router = APIRouter(
     prefix="/api/v1",
     tags=["Skin", "Bot"],
     dependencies=[Depends(valide_secret_bot_token)]
)



@skin_router.get(
     path="/skin", 
     response_model=SkinModel,
     responses=router_responses(
          SkinNotFoundError,
          AuthError,
          SecretTokenError,
          ServerError
     ),
     summary="Получение данных скина."
)
async def get_skin(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     skin_name: str
):
     result = await service.get_skin(
          async_session=async_session,
          redis_session=redis_session,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result
     
     
          
     
@skin_router.get(
     path="/skin/search", 
     response_model=SkinsPage,
     responses=router_responses(
          SkinNotFoundError,
          OffsetError,
          AuthError,
          SecretTokenError,
          ServerError
     ),
     summary="Поиск скинов по названию."
)
async def search_skin(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     query: str,
     offset: int = Query(ge=0),
     limit: int = Query(ge=1, le=50)
):
     result = await service.search_skin(
          async_session=async_session,
          redis_session=redis_session,
          query=query,
          offset=offset,
          limit=limit
     )
     if isresponse(result):
          return result.response()
     return result
     
     
     
@skin_router.get(
     path="/skin/history", 
     response_model=SkinHistoryTimePartModel,
     responses=router_responses(
          SkinNotFoundError,
          AuthError,
          SecretTokenError,
          ServerError
     ),
     summary="Получение истории изменения цены скина."
)
async def skin_history(
     service: Annotated[SkinService, Depends(get_skin_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     skin_name: str
):
     result = await service.skin_history(
          async_session=async_session,
          redis_session=redis_session,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result
