import uuid

from typing import Type

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.repositories.abc_condition import BaseWhereCondition

from app.services.abc import BaseUserLikeSkinsService
from app.responses.abc import BaseResponse
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginateSkinsModel
from app.schemas.enums import WhereConditionEnum
from app.schemas.presentation.dto import UserLikeSkinDTOPresentation
from app.responses import (
     DataNotExistsError,
     DeleteSuccess,
     DataAlreadyExistsError,
     CreateSuccess
)

class UserLikeSkinsService(BaseUserLikeSkinsService):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
     
     
     async def get_likes_skins(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginateSkinsModel,
          **kwargs
     ) -> SkinsPage[UserLikeSkinDTOPresentation]:
          async with uow:
               async with cache:
                    skins, skins_count = await uow.user_like_skin_repo.read_many(
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix=f"user_like_skins-{token_payload.uuid}"),
                         relationship_columns=["skin", "collections"],
                         joinedload_relship_columns=["skin", "collections"],
                         where={
                              "default": [self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)],
                              "skin": paginate_data.generate_conditions(condition=self.condition),
                         },
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         order_by={"skin": [(paginate_data.order_by.value, paginate_data.order_by_mode.value)]},
                         count=True
                    )
          return SkinsPage(
               pages=skins_count,
               current_page=paginate_data.offset,
               skins=[skin.as_presentation() for skin in skins],
               skins_on_page=paginate_data.limit
          ).serialize()
          
          
     async def create_like_skin(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str,
          **kwargs
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin = await uow.user_like_skin_repo.read(
                         where={
                              "default": [
                                   self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ),
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)
                              ]
                         }
                    )
                    if skin is None:
                         await uow.user_like_skin_repo.create(
                              values={
                                   "uuid": uuid.uuid4(),
                                   "user_uuid": token_payload.uuid,
                                   "market_hash_name": skin_name
                              },
                              cache=cache,
                              cache_keys=[f"user_like_skins-{token_payload.uuid}"]
                         )
                         await uow.commit()
                         return CreateSuccess
                    return DataAlreadyExistsError

          
     async def delete_like_skin(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str,
          **kwargs
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    result = await uow.user_like_skin_repo.delete(
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ)
                              ]
                         },
                         cache=cache,
                         cache_keys=[f"user_like_skins:{token_payload.uuid}"],
                         returning="user_uuid"
                    )
                    await uow.commit()
          if result:
               return DeleteSuccess
          return DataNotExistsError
                    