from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse

from app.api.v1.routers.dependency import get_async_session, get_redis_session
from app.core.template import templates
from app.infrastracture.redis import RedisPool
from app.responses import isresponse
from .service import TemplateService, get_template_service
from .depend import valide_token



template_router = APIRouter(
     prefix="/main",
     tags=["Template"]
)


@template_router.get(path="/profile")
async def profile(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     service: Annotated[TemplateService, Depends(get_template_service)],
     uuid: Annotated[tuple[str, str | None] | None, Depends(valide_token)],
     request: Request
) -> HTMLResponse:
     if uuid is None:
          return templates.TemplateResponse(
               request=request,
               name="auth.html"
          )
     user = await service.profile(
          redis_session=redis_session,
          async_session=async_session,
          uuid=uuid[0]
     )
     if isresponse(user):
          return templates.TemplateResponse(
               request=request,
               name="auth.html"
          )
     return templates.TemplateResponse(
          name="profile.html",
          context={
               "request": request,
               "token": uuid[1],
               "steam_avatar": user.steam_avatar,
               "steam_name": user.steam_name
          }
     )