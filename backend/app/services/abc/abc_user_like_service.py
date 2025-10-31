from typing import Protocol

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork

from app.responses.abc import BaseResponse
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginateUserLikeSkinsModel
from app.schemas.dto import UserLikeSkinDTO


class BaseUserLikeSkinsService(Protocol):
     
     
     async def get_likes_skins(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginateUserLikeSkinsModel
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