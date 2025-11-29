from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import RedirectResponse
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from pydantic import HttpUrl

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.services.abc import BaseAuthService
from app.api.v1.dependency.rate_limit import RateLimitDepend
from app.schemas import (
     ExchangeKeyModel, 
     AccessTokenModel, 
     TelegramDataModel, 
     JWTTokenPayloadModel
)
from app.responses import (
     HttpError,
     isresponse,
     router_responses,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     LoginError,
     LoginSuccess,
     InvalidCodeError,
     TooManyRequestError
)



auth_router = APIRouter(
     prefix="/api/v1/auth",
     tags=["Auth"],
     route_class=DishkaRoute
)



@auth_router.get(
     path="/steam/login",  
     responses=router_responses(ServerError),
     summary="Перенаправление на страницу входа через Steam аккаунт.",
)
async def steam_redirect(
     service: FromDishka[BaseAuthService],
     redirect_url: HttpUrl | None = None
):
     return await service.steam_login(redirect_url=redirect_url)  
     
     
     
@auth_router.get(
     path="/steam/processing", 
     responses=router_responses(
          HttpError,
          LoginError,
          ServerError
     ),
     summary="Сюда происходит перенаправление после входа в Steam аккаунт."
)
async def steam_processing(
     request: Request,
     response: Response,
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
     response.set_cookie("access_token", result)
     
     

@auth_router.get(
     path="/exchange",
     response_model=AccessTokenModel,
     responses=router_responses(
          ServerError,
          InvalidCodeError,
          TooManyRequestError
     ),
     summary="Обмен кода на jwt token.",
     dependencies=[Depends(RateLimitDepend(1, timedelta(seconds=1), "exchange"))]
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
          JWTTokenInvalidError,
          TooManyRequestError
     ),
     summary="Получения кода для привязки Telegram аккаунта.",
     dependencies=[Depends(RateLimitDepend(1, timedelta(seconds=1), "tg_exchange"))]
)
async def telegram_exchange(
     token_payload: FromDishka[JWTTokenPayloadModel],
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
     summary="Привязка Telegram аккаунта.",
     dependencies=[Depends(RateLimitDepend(1, timedelta(seconds=1), "tg_processing"))]
)
async def telegram_processing(
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     service: FromDishka[BaseAuthService],
     telegram_data: Annotated[TelegramDataModel, Form()],
     code: str,
):
     result = await service.telegram_processing(
          telegram_data=telegram_data,
          code=code,
          cache=cache,
          uow=uow
     )
     return result.response()