
from app.db.repository import UserRepository
from app.schemas import UserModel, SteamItem
from app.responses import UserNotFoundError
from app.responses.abstract import AbstractResponse
from app.infrastracture.https.steam import HttpSteamClient


class UserService:
     def __init__(self):
          self.user_repository = UserRepository
          self.http_steam_client = HttpSteamClient()
          
     
     async def get_user(self, uuid: str) -> UserModel | AbstractResponse:
          user = await self.user_repository.read(uuid=uuid)
          if user is None:
               return UserNotFoundError
          return user
     
     
     async def get_user_steam_inventory(self, uuid: str) -> list[SteamItem] | AbstractResponse:
          user = await self.user_repository.read(uuid=uuid)
          if user is None:
               return UserNotFoundError
          
          return await self.http_steam_client.get_steam_inventory(
               steamid=user.steam_id
          )
          
     
     
async def get_user_service() -> UserService:
     return UserService()