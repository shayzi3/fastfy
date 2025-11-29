from typing import Type

from app.repositories.abc_condition import BaseWhereCondition
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse
from app.services.abc import BaseNotificationService
from app.responses import ArgumentError

from app.schemas.enums import WhereConditionEnum
from app.schemas import JWTTokenPayloadModel, NotifyFiltersModel
from app.schemas.dto import UserNotifyDTO



class NotificationService(BaseNotificationService):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
          
          
     async def get_users_notify(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          filters_data: NotifyFiltersModel
     ) -> list[UserNotifyDTO] | BaseResponse:
          if not filters_data.non_nullable():
               return ArgumentError
          
          async with uow:
               async with cache:
                    notifies, _ = await uow.user_notify_repo.read_many(
                         cache=cache,
                         cache_key=filters_data.cache_key(f"user_notify:{token_payload.uuid}"),
                         joinedload_relship_columns=["user"],
                         where={
                              "default": filters_data.generate_conditions(
                                   condition=self.condition,
                                   additional_conditions=[
                                        self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)
                                   ]
                              )
                         }
                    )
                    return [notify.as_presentation() for notify in notifies]
                    