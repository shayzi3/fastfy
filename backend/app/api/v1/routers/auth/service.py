import uuid

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from steam_openid import SteamOpenID

from app.core import my_config
from app.core.utils import id_with_symbols
from app.responses.abstract import AbstractResponse
from app.db.repository import UserRepository, UserNotifyRepository
from app.infrastracture.https.steam import HttpSteamClient
from app.infrastracture.redis import RedisPool
from app.responses import (
     SteamLoginError, 
     isresponse,
     TelegramLoginSuccess,
     TelegramLoginError
)
from .schema import TelegramData




class AuthService:
     def __init__(self):
          self.openid = SteamOpenID(
               realm=my_config.steam_return_to,
               return_to=my_config.steam_return_to
          )
          self.steam_http_client = HttpSteamClient()
          self.user_repository = UserRepository
          self.notify_repository = UserNotifyRepository
          
          
     async def steam_login(self) -> str:
          return self.openid.get_redirect_url()
     
     
     async def steam_processing(
          self, 
          query_params: Any,
          async_session: AsyncSession,
          redis_pool: RedisPool
     ) -> AbstractResponse | str:
          steamid = self.openid.validate_results(query_params)
          if steamid is None:
               return SteamLoginError
          
          steamid = int(steamid)
          exists = await self.user_repository.read(
               session=async_session,
               steam_id=steamid
          )
          if exists is None:
               steamdata = await self.steam_http_client.get_steam_profile(steamid)
               if isresponse(steamdata):
                    return steamdata
               
               steam_name, steam_avatar = steamdata
               await self.user_repository.create(
                    session=async_session,
                    uuid=uuid.uuid4(),
                    steam_id=steamid,
                    steam_name=steam_name,
                    steam_avatar=steam_avatar
               )
          id = await id_with_symbols()
          await redis_pool.set(
               name=id,
               value=steamid,
               ex=120
          )
          return id
     
     
     async def telegram_processing(
          self,
          code: str,
          data: TelegramData,
          session: AsyncSession,
          redis_session: RedisPool
     ) -> AbstractResponse:
          steam_id = await redis_session.get(code)
          if steam_id is not None:
               await redis_session.delete(code)
               
               user_uuid = await self.user_repository.update(
                    session=session,
                    where={"steam_id": int(steam_id)},
                    **data.model_dump()
               )
               if user_uuid:
                    await redis_session.set(
                         name=str(data.telegram_id),
                         value=str(user_uuid)
                    )
               return TelegramLoginSuccess
          return TelegramLoginError
          
          
     
     
     
async def get_auth_service() -> AuthService:
     return AuthService()