from typing import Protocol, Type

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.repositories.abc_condition import BaseWhereCondition

from app.responses.abc import BaseResponse
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginateSkinsModel
from app.schemas.dto import UserLikeSkinDTO


class BaseUserLikeSkinsService(Protocol):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
      
     
     async def get_likes_skins(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[UserLikeSkinDTO]:
          ...
          
          
     async def create_like_skin(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str
     ) -> BaseResponse:
          ...
          
          
     async def delete_like_skin(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str
     ) -> BaseResponse:
          ...