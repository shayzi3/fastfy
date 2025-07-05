from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from steam_openid import SteamOpenID

from app.core import my_config
from app.responses.abstract import AbstractResponse
from app.db.repository import UserRepository
from app.infrastracture.https.steam import HttpSteamClient
from app.infrastracture.redis import RedisPool
from app.responses import (
     SteamLoginError, 
     isresponse,
     TelegramProcessError,
     TelegramProcessSuccess
)
from app.core.utils import (
     generate_payload_deeplink,
     generate_processid,
     generate_session
)
from .schema import SteamLoginUser




class AuthService:
     def __init__(self):
          self.openid = SteamOpenID(
               realm=my_config.steam_return_to,
               return_to=my_config.steam_return_to
          )
          self.steam_http_client = HttpSteamClient()
          self.user_repository = UserRepository
          
          
     async def steam_redirest(self) -> str:
          return self.openid.get_redirect_url()
     
     
     async def steam_processing(
          self, 
          query_params: Any,
          async_session: AsyncSession,
          redis_session: RedisPool
     ) -> AbstractResponse | SteamLoginUser:
          steamid = self.openid.validate_results(query_params)
          if steamid is None:
               return SteamLoginError
          
          exists = await self.user_repository.read(
               session=async_session,
               steam_id=int(steamid)
          )
          if exists is None:
               steamdata = await self.steam_http_client.get_steam_profile(steamid)
               if isresponse(steamdata):
                    return steamdata
               
               steam_name, steam_avatar = steamdata
               uuid = await self.user_repository.create(
                    session=async_session,
                    steam_id=steamid,
                    steam_name=steam_name,
                    steam_avatar=steam_avatar
               )
          session = await generate_session()
          await redis_session.set(
               name=f"session:{session}",
               value=uuid if exists is None else exists.uuid,
               ex=120
          )
          return session
          
     
     async def telegram_login(
          self, 
          user_uuid: str, 
          redis_session: RedisPool
     ) -> str:
          payload_deeplink = await generate_payload_deeplink()
          processid = await generate_processid()
          
          async with redis_session.pipeline() as pool:
               await pool.set(
                    name=payload_deeplink,
                    value=processid,
                    ex=180
               )
               await pool.set(
                    name=processid,
                    value=user_uuid,
                    ex=180
               )
               await pool.execute()
               
          deeplink = my_config.bot_deep_link + payload_deeplink
          return deeplink
          
          
     async def telegram_processing(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          processid: str,
          telegram_id: int,
          telegram_username: str
     ):
          user_uuid = await redis_session.get(processid)
          if user_uuid is not None:
               await redis_session.delete(processid)
               await self.user_repository.update(
                    session=async_session,
                    redis_session=redis_session,
                    delete_redis_values=[f"user:{user_uuid}", f"user_rel:{user_uuid}"],
                    where={"uuid": user_uuid},
                    telegram_id=telegram_id,
                    telegram_username=telegram_username
               )
               return TelegramProcessSuccess
          return TelegramProcessError
               
          
               
          
     
     
     
async def get_auth_service() -> AuthService:
     return AuthService()