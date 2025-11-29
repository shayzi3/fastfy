from typing import Type

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.services.abc.abc_user_service import BaseUserService
from app.infrastracture.https.clients.steam.abc import BaseSteamClient
from app.responses.abc import BaseResponse
from app.repositories.abc_condition import BaseWhereCondition

from app.schemas import SkinsPage, JWTTokenPayloadModel, PatchUserModel
from app.schemas.enums import WhereConditionEnum
from app.schemas.dto import UserDTO
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses import (
     isresponse, 
     ArgumentError,
     NotFoundError,
     UpdateSuccess,
     UpdateError
)


class UserService(BaseUserService):
     def __init__(
          self,
          steam_client: BaseSteamClient,
          condition: Type[BaseWhereCondition]
     ):
          self.http_steam_client = steam_client      
          self.condition = condition    
     
     
     async def get_user(
          self, 
          cache: Cache,
          uow: BaseUnitOfWork,
          token_payload: JWTTokenPayloadModel
     ) -> UserDTO | BaseResponse:
          async with uow:
               async with cache:
                    user = await uow.user_repo.read(
                         where={"default": [self.condition("uuid", token_payload.uuid, WhereConditionEnum.EQ)]},
                         cache=cache,
                         cache_key=f"user:{token_payload.uuid}",
                    )
          if user is None:
               return NotFoundError
          return user.as_presentation()
     
     
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
          if not data.get_update_field_values():
               return ArgumentError
          
          async with uow:
               async with cache:
                    result = await uow.user_repo.update(
                         cache=cache,
                         cache_keys=[f"user:{token_payload.uuid}"],
                         where={"default": [self.condition("uuid", token_payload.uuid, WhereConditionEnum.EQ)]},
                         values=data.non_nullable(),
                         returning="uuid",
                    )
               if result:
                    return UpdateSuccess
          return UpdateError