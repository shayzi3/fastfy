from typing import Protocol

from app.responses.abc import BaseResponse
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.https.clients.steam.abc import BaseSteamClient

from app.schemas.dto import UserDTO
from app.schemas import (
     JWTTokenPayloadModel, 
     SkinsPage, 
     SteamItemModel, 
     PatchUserModel
)



class BaseUserService(Protocol):
     def __init__(
          self, 
          steam_client: BaseSteamClient,
     ):
          self.steam_client = steam_client
          
     
     async def get_user(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          token_payload: JWTTokenPayloadModel
     ) -> UserDTO | BaseResponse:
          ...
          
     async def get_user_steam_inventory(
          self,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          offset: int,
          limit: int
     ) -> SkinsPage[SteamItemModel] | BaseResponse:
          ...
          
          
     async def patch_user(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          data: PatchUserModel,
          token_payload: JWTTokenPayloadModel
     ) -> BaseResponse:
          ...