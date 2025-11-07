from typing import Protocol, Type

from app.repositories.abc_condition import BaseWhereCondition
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse

from app.schemas import JWTTokenPayloadModel, NotifyFiltersModel
from app.schemas.dto import UserNotifyDTO



class BaseNotificationService(Protocol):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
          
          
     async def get_users_notify(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          filter_data: NotifyFiltersModel
     ) -> list[UserNotifyDTO] | BaseResponse:
          ...