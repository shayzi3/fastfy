

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.services.abc.abc_user_service import BaseUserService
from app.infrastracture.https.clients.steam.abc import BaseSteamClient
from app.responses.abc import BaseResponse

from app.schemas import SkinsPage, JWTTokenPayloadModel, PatchUserModel
from app.schemas.dto import UserDTO
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses import (
     UserNotFoundError, 
     UserUpdateSuccess, 
     isresponse, 
     ArgumentError,
     UserUpdateError
)


class UserService(BaseUserService):
     def __init__(
          self,
          steam_client: BaseSteamClient,
     ):
          self.http_steam_client = steam_client          
     
     
     async def get_user(
          self, 
          cache: Cache,
          uow: BaseUnitOfWork,
          token_payload: JWTTokenPayloadModel
     ) -> UserDTO | BaseResponse:
          async with uow:
               async with cache:
                    user = await uow.user_repo.read(
                         where={"uuid": token_payload.uuid},
                         cache=cache,
                         cache_key=f"user:{token_payload.uuid}",
                    )
          if user is None:
               return UserNotFoundError
          return user
     
     
     async def get_user_steam_inventory(
          self, 
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          offset: int,
          limit: int
     ) -> SkinsPage | BaseResponse:
          async with cache:
               result = await self.http_steam_client.get_steam_inventory(
                    steamid=token_payload.steam_id,
                    cache=cache,
                    offset=offset,
                    limit=limit,
               )
          if isresponse(result):
               return result
          return result
     
     
     async def patch_user(
          self, 
          cache: Cache, 
          uow: BaseUnitOfWork, 
          data: PatchUserModel,
          token_payload: JWTTokenPayloadModel
     ) -> BaseResponse:
          if not data.non_nullable():
               return ArgumentError
          
          async with uow:
               async with cache:
                    result = await uow.user_repo.update(
                         cache=cache,
                         cache_keys=[f"user:{token_payload.uuid}"],
                         where={"uuid": token_payload.uuid},
                         values=data.non_nullable(),
                         returning=True,
                    )
               if result:
                    return UserUpdateSuccess
          return UserUpdateError