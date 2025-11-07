from typing import Any, Protocol, Type

from fastapi.responses import RedirectResponse

from app.core.security.abc import BaseJWTSecurity
from app.infrastracture.openid.abc import BaseOpenID
from app.infrastracture.https.clients.steam.abc import BaseSteamClient
from app.responses.abc import BaseResponse
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_condition import BaseWhereCondition
from app.schemas import (
     ExchangeKeyModel,
     AccessTokenModel,
     JWTTokenPayloadModel,
     TelegramDataModel
)


class BaseAuthService(Protocol):
     
     def __init__(
          self,
          steam_client: BaseSteamClient,
          jwt_security: BaseJWTSecurity,
          openid: BaseOpenID,
          condition: Type[BaseWhereCondition]
     ):
          self.steam_client = steam_client
          self.jwt_security = jwt_security
          self.openid = openid
          self.condition = condition
     
     
     async def steam_login(
          self, 
          redirect_url: str
     ) -> RedirectResponse:
          ...
          
          
     async def steam_processing(
          self,
          uow: BaseUnitOfWork,
          query_params: Any,
          cache: Cache,
          redirect_url: str= ""
     ) -> BaseResponse | ExchangeKeyModel | str:
          ...
          
          
     async def exchange(
          self,
          code: str,
          cache: Cache
     ) -> BaseResponse | AccessTokenModel:
          ...
          
          
     async def telegram_exchange(
          self,
          token_payload: JWTTokenPayloadModel,
          cache: Cache
     ) -> ExchangeKeyModel:
          ...
          
          
     async def telegram_processing(
          self,
          telegram_data: TelegramDataModel,
          cache: Cache,
          uow: BaseUnitOfWork,
          code: str
     ) -> BaseResponse:
          ...