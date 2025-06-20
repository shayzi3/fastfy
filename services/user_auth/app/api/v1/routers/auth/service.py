import uuid

from typing import Any
from steam_openid import SteamOpenID

from app.core import my_config
from app.schemas import SteamLoginUser
from app.responses.abstract import AbstractResponse
from app.db.repository import UserRepository
from app.infrastracture.https import HttpSteamClient
from app.responses import (
     SteamLoginError, 
     isresponse
)




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
          
     
     
     
     async def telegram_login(self):
          ...
          
          
          
     async def telegram_processing(self):
          ...
               
          
               
          
     
     
     
async def get_auth_service() -> AuthService:
     return AuthService()