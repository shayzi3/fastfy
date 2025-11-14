from typing import Annotated
from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.services.abc import BaseNotificationService

from app.schemas.presentation.dto import UserNotifyDTOPresentation
from app.schemas import NotifyFiltersModel, JWTTokenPayloadModel
from app.responses import (
     isresponse, 
     router_responses,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     ArgumentError
)



notification_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User Notification"],
     route_class=DishkaRoute
)



@notification_router.get(
     path="/notify", 
     response_model=list[UserNotifyDTOPresentation],
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          ArgumentError
     ),
     summary="Получение уведомлений пользователя."
)
async def get_notify_new(
     token_payload: FromDishka[JWTTokenPayloadModel],
     service: FromDishka[BaseNotificationService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     filter_data: Annotated[NotifyFiltersModel, Form()]
):
     result = await service.get_users_notify(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          filter_data=filter_data
     )
     if isresponse(result):
          return result.response()
     return result
     
     