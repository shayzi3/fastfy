from typing import Protocol, Type

from app.responses.abc import BaseResponse
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.https.clients.steam.abc import BaseSteamClient
from app.repositories.abc_condition import BaseWhereCondition

from app.schemas.presentation.dto import UserDTOPresentation
from app.schemas import (
     JWTTokenPayloadModel, 
     SkinsPage, 
     SteamInventorySkinModel, 
     PatchUserModel,
)



class BaseUserService(Protocol):
     def __init__(
          self, 
          steam_client: BaseSteamClient,
          condition: Type[BaseWhereCondition]
     ):
          self.steam_client = steam_client
          self.condition = condition
          
     
     async def get_user(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          token_payload: JWTTokenPayloadModel
     ) -> UserDTOPresentation | BaseResponse:
          ...
     
     async def get_user_steam_inventory(
          self,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          offset: int,
          limit: int
     ) -> SkinsPage[SteamInventorySkinModel] | BaseResponse:
          ...
          
     async def patch_user(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          data: PatchUserModel,
          token_payload: JWTTokenPayloadModel
     ) -> BaseResponse:
          ...