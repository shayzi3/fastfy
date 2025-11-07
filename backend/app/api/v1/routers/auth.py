from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from pydantic import HttpUrl

from app.core.security.abc import BaseJWTSecurity
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.services.abc import BaseAuthService
from app.schemas import ExchangeKeyModel, AccessTokenModel, TelegramDataModel
from app.responses import (
     HttpError,
     isresponse,
     router_responses,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     LoginError,
     LoginSuccess,
     InvalidCodeError
)



auth_router = APIRouter(
     prefix="/api/v1/auth",
     tags=["Auth"],
     route_class=DishkaRoute
)



@auth_router.get(
     path="/steam/login", 
     response_class=RedirectResponse,
     responses=router_responses(ServerError),
     summary="Перенаправление на страницу входа через Steam аккаунт."
)
async def steam_redirect(
     service: FromDishka[BaseAuthService],
     redirect_url: HttpUrl | None = None
):
     return await service.steam_login(redirect_url=redirect_url)  
     
     
     
@auth_router.get(
     path="/steam/processing", 
     response_class=RedirectResponse,
     response_model=ExchangeKeyModel,
     responses=router_responses(
          HttpError,
          LoginError,
          ServerError
     ),
     summary="Сюда происходит перенаправление после входа в Steam аккаунт."
)
async def steam_processing(
     request: Request,
     service: FromDishka[BaseAuthService],
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     redirect_url: HttpUrl | None = None
):
     result = await service.steam_processing(
          uow=uow,
          query_params=request.query_params,
          cache=cache,
          redirect_url=redirect_url
     )
     if isresponse(result):
          return result.response()
     
     if redirect_url:
          return RedirectResponse(url=result)
     return result
     
     
     
@auth_router.get(
     path="/exchange",
     response_model=AccessTokenModel,
     responses=router_responses(
          ServerError,
          InvalidCodeError
     ),
     summary="Обмен кода на jwt token."
)
async def exchange(
     code: str,
     cache: FromDishka[Cache],
     service: FromDishka[BaseAuthService]
):
     result = await service.exchange(
          code=code,
          cache=cache
     )
     if isresponse(result):
          return result.response()
     return result



@auth_router.get(
     path="/telegram/exchange",
     response_model=ExchangeKeyModel,
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError
     ),
     summary="Получения кода для привязки Telegram аккаунта."
)
async def telegram_exchange(
     token_payload: FromDishka[BaseJWTSecurity],
     cache: FromDishka[Cache],
     service: FromDishka[BaseAuthService]
):
     return await service.telegram_exchange(
          token_payload=token_payload,
          cache=cache
     )
     
     
     
@auth_router.patch(
     path="/telegram/processing",
     responses=router_responses(
          ServerError,
          LoginError,
          LoginSuccess
     ),
     summary="Привязка Telegram аккаунта."
)
async def telegram_processing(
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     service: FromDishka[BaseAuthService],
     code: str,
     telegram_data: Annotated[TelegramDataModel, Form()]
):
     result = await service.telegram_processing(
          telegram_data=telegram_data,
          code=code,
          cache=cache,
          uow=uow
     )
     return result.response()