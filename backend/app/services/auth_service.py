import uuid

from typing import Any, Type
from urllib.parse import urlparse, urlencode

from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from app.core import my_config
from app.responses.abc import BaseResponse
from app.infrastracture.https.clients.steam import BaseSteamClient
from app.infrastracture.openid.abc import BaseOpenID
from app.core.security.abc import BaseJWTSecurity
from app.infrastracture.cache.abc import Cache
from app.utils.generator import async_random_string_generator
from app.repositories.abc_uow import BaseUnitOfWork
from .abc.abc_auth_service import BaseAuthService
from app.repositories.abc_condition import BaseWhereCondition
from app.schemas.enums import WhereConditionEnum
from app.responses import (
     LoginError, 
     isresponse,
     LoginSuccess,
     InvalidCodeError
)
from app.schemas import (
     TelegramDataModel, 
     AccessTokenModel, 
     JWTTokenPayloadModel, 
     ExchangeKeyModel
)



class AuthService(BaseAuthService):
     def __init__(
          self, 
          steam_client: BaseSteamClient, 
          jwt_security: BaseJWTSecurity,
          openid: BaseOpenID,
          condition: Type[BaseWhereCondition]
     ):
          self.openid = openid
          self.steam_client = steam_client
          self.jwt_security = jwt_security
          self.condition = condition
          
          
     async def steam_login(self, redirect_url: HttpUrl | None) -> RedirectResponse:
          url_steam_processing = my_config.steam_return_to
          if redirect_url:
               url_steam_processing += f"?{urlencode({'redirect_url': str(redirect_url)})}"
          
          url = await self.openid.construct_url(return_to=url_steam_processing)
          return await self.openid.redirect_user(url=url)
          
     
     async def steam_processing(
          self, 
          uow: BaseUnitOfWork,
          query_params: Any,
          cache: Cache,
          redirect_url: HttpUrl | None
     ) -> BaseResponse | ExchangeKeyModel | str:
          steamid = await self.openid.validate_results(query_params)
          if steamid is False:
               return LoginError
          
          steamid = int(steamid)
          async with uow:
               account = await uow.user_repo.read(
                    where={
                         "default": [
                              self.condition("steam_id", steamid, WhereConditionEnum.EQ)
                         ]
                    }
               )
               if account is None:
                    steam_data = await self.steam_client.get_steam_profile(
                         steam_id=steamid
                    )
                    if isresponse(steam_data):
                         return steam_data
                    
                    user_uuid = uuid.uuid4()
                    await uow.user_repo.create(
                         values={
                              "uuid": user_uuid,
                              "steam_id": steamid,
                              **steam_data.model_dump()
                         }
                    )
                    await uow.commit()
               
          jwt_token = await self.jwt_security.encode(
               data={
                    "uuid": user_uuid if not account else account.uuid,
                    "steam_id": steamid,
                    "steam_name": steam_data.steam_name if not account else account.steam_name,
                    "steam_avatar": steam_data.steam_avatar if not account else steam_data.steam_avatar
               }
          )
          key_for_exchange = await async_random_string_generator(
               max_length=25,
               use_digits=True,
               use_letters=True
          )
          async with cache:
               await cache.set(key=key_for_exchange, value=jwt_token, ex=300)
               
          if redirect_url:
               redirect_url_parse = urlparse(url=str(redirect_url))
               separator = "?" if not redirect_url_parse.query else "&"
               return str(redirect_url) + separator + urlencode({"code": key_for_exchange})
          return ExchangeKeyModel(exchange_key=key_for_exchange)
               
     
     async def exchange(
          self,
          code: str,
          cache: Cache
     ) -> AccessTokenModel | BaseResponse:
          async with cache:
               jwt_token = await cache.get(key=code)
               
               if jwt_token:
                    await cache.delete(code)
                    return AccessTokenModel(access_token=jwt_token)
          return InvalidCodeError
     
     
     async def telegram_exchange(
          self,
          token_payload: JWTTokenPayloadModel,
          cache: Cache
     ) -> ExchangeKeyModel:
          async with cache:
               key_for_exchange = await async_random_string_generator(
                    max_length=25,
                    use_digits=True,
                    use_letters=True
               )
               await cache.set(key=key_for_exchange, value=token_payload.uuid, ex=180)
          return ExchangeKeyModel(exchange_key=key_for_exchange)
     
     
     async def telegram_processing(
          self,
          telegram_data: TelegramDataModel,
          code: str,
          cache: Cache,
          uow: BaseUnitOfWork
     ) -> BaseResponse:
          async with cache:
               user_uuid = await cache.get(key=code)
               if user_uuid:
                    async with uow:
                         is_update = await uow.user_repo.update(
                              cache=cache,
                              cache_keys=[f"user:{user_uuid}"],
                              where={"default": [self.condition("uuid", user_uuid, WhereConditionEnum.EQ)]},
                              returning="uuid",
                              values=telegram_data.model_dump()
                         )
                         await uow.commit()
                         if not is_update:
                              return LoginError
                    return LoginSuccess
               return LoginError
     
     
          
          
     