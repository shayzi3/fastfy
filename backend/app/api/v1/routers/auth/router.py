from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse

from app.responses import (
     HttpError,
     SteamLoginError,
     TelegramLoginError,
     TelegramLoginSuccess,
     isresponse,
     router_responses,
     SecretTokenError,
     ServerError
)
from app.core.template import templates
from app.infrastracture.redis import RedisPool, get_redis_session
from app.db.session import AsyncSession, get_async_session
from ..dependency import valide_secret_bot_token
from .service import get_auth_service, AuthService
from .schema import TelegramData



auth_router = APIRouter(
     prefix="/api/v1",
     tags=["Auth", "Bot"]
)



@auth_router.get(
     path="/auth/steam/login", 
     response_class=RedirectResponse,
     summary="Перенаправление на страницу входа через Steam аккаунт."
)
async def steam_redirect(
     service: Annotated[AuthService, Depends(get_auth_service)]
):
     url = await service.steam_login()
     return RedirectResponse(url=url)
      
     
     
@auth_router.get(
     path="/auth/steam/processing", 
     response_class=HTMLResponse,
     responses=router_responses(
          HttpError,
          SteamLoginError,
          ServerError
     ),
     summary="Сюда происходит перенаправление после входа в Steam аккаунт."
)
async def steam_processing(
     request: Request,
     service: Annotated[AuthService, Depends(get_auth_service)],
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_pool: Annotated[RedisPool, Depends(get_redis_session)]
):
     result = await service.steam_processing(
          query_params=request.query_params,
          async_session=async_session,
          redis_pool=redis_pool
     )
     if isresponse(result):
          return result.response()
     
     return templates.TemplateResponse(
          name="code.html",
          context={
               "request": request,
               "code": result
          }
     )


@auth_router.post(
     path="/auth/telegram/processing",
     responses=router_responses(
          TelegramLoginSuccess,
          TelegramLoginError,
          SecretTokenError,
          ServerError
     ),
     dependencies=[Depends(valide_secret_bot_token)],
     summary="Создание текущего аккаунта."
)
async def telegram_processing(
     code: str,
     data: Annotated[TelegramData, Form()],
     session: Annotated[AsyncSession, Depends(get_async_session)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     service: Annotated[AuthService, Depends(get_auth_service)]
):
     result = await service.telegram_processing(
          code=code,
          data=data,
          session=session,
          redis_session=redis_session
     )
     return result.response()