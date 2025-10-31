import uuid

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork

from app.services.abc import BaseUserLikeSkinsService
from app.responses.abc import BaseResponse
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginateUserLikeSkinsModel
from app.schemas.dto import UserLikeSkinDTO
from app.responses import (
     SkinDeleteSuccess,
     SkinNotExistsError,
     SkinAlreadyExistsError,
     SkinCreateSuccess
)

class UserLikeSkinsService(BaseUserLikeSkinsService):
     
     
     async def get_likes_skins(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginateUserLikeSkinsModel,
          **kwargs
     ) -> SkinsPage[UserLikeSkinDTO]:
          async with uow:
               async with cache:
                    skins, skins_count = await uow.user_like_skin_repo.paginate(
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix=f"user_like_skins-{token_payload.uuid}"),
                         where={"user_uuid": token_payload.uuid}
                    )
          return SkinsPage(
               pages=skins_count,
               current_page=paginate_data.offset,
               skins=skins,
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
                         where={"market_hash_name": skin_name, "user_uuid": token_payload.uuid}
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
                         return SkinCreateSuccess
                    return SkinAlreadyExistsError

          
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
                         where={"user_uuid": token_payload.uuid, "market_hash_name": skin_name},
                         cache=cache,
                         cache_keys=[f"user_like_skins-{token_payload.uuid}"],
                         returning=True
                    )
          if result:
               return SkinDeleteSuccess
          return SkinNotExistsError
                    