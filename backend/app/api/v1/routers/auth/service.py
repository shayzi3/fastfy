import uuid

from typing import Any
from steam_openid import SteamOpenID

from app.core import my_config
from app.schemas import SteamLoginUser
from app.responses.abstract import AbstractResponse
from app.db.repository import UserRepository
from app.infrastracture.https import HttpSteamClient
from app.infrastracture.redis import RedisPool
from app.responses import (
     SteamLoginError, 
     isresponse,
     TelegramProcessError,
     TelegramProcessSuccess
)
from app.core.utils import (
     generate_payload_deeplink,
     generate_processid
)




class AuthService:
     def __init__(self):
          self.openid = SteamOpenID(
               realm=my_config.steam_return_to,
               return_to=my_config.steam_return_to
          )
          self.steam_http_client = HttpSteamClient()
          self.redis = RedisPool()
          self.user_repository = UserRepository
          
          
     async def steam_redirest(self) -> str:
          return self.openid.get_redirect_url()
     
     
     async def steam_processing(
          self, 
          query_params: Any
     ) -> AbstractResponse | SteamLoginUser:
          steamid = self.openid.validate_results(query_params)
          if steamid is None:
               return SteamLoginError
          
          steamid = int(steamid)
          exists = await self.user_repository.read(steam_id=steamid)
          if exists is None:
               steamdata = await self.steam_http_client.get_steam_profile(steamid)
               if isresponse(steamdata):
                    return steamdata
               
               uuid4 = uuid.uuid4()
               steam_name, steam_avatar = steamdata
               await self.user_repository.insert(
                    uuid=uuid4,
                    steam_id=steamid,
                    steam_name=steam_name,
                    steam_avatar=steam_avatar
               )
               
          return SteamLoginUser(
               uuid=str(exists.uuid) if exists else str(uuid4),
               steam_name=exists.steam_name if exists else steam_name,
               steam_avatar=exists.steam_avatar if exists else steam_avatar,
          )
          
     
     async def telegram_login(self, user_uuid: str) -> str:
          payload_deeplink = await generate_payload_deeplink()
          processid = await generate_processid()
          await self.redis.set(
               name=payload_deeplink,
               value=processid,
               ex=180
          )
          await self.redis.set(
               name=processid,
               value=user_uuid,
               ex=180
          )
          deeplink = my_config.bot_deep_link + payload_deeplink
          return deeplink
          
          
     async def telegram_processing(
          self,
          processid: str,
          telegram_id: int,
          telegram_username: str
     ):
          user_uuid = await self.redis.get(processid)
          if user_uuid is not None:
               await self.redis.delete(processid)
               await self.user_repository.update(
                    where={"uuid": user_uuid},
                    telegram_id=telegram_id,
                    telegram_username=telegram_username
               )
               return TelegramProcessSuccess
          return TelegramProcessError
               
          
               
          
     
     
     
async def get_auth_service() -> AuthService:
     return AuthService()