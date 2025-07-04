from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.db.repository import UserRepository
from app.schemas import UserModel, SteamItem
from app.responses import UserNotFoundError
from app.responses.abstract import AbstractResponse
from app.infrastracture.https.steam import HttpSteamClient


class UserService:
     def __init__(self):
          self.user_repository = UserRepository
          self.http_steam_client = HttpSteamClient()
          
     
     async def get_user(
          self, 
          async_session: AsyncSession,
          redis_session: RedisPool,
          uuid: str
     ) -> UserModel | AbstractResponse:
          user = await self.user_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"user:{uuid}",
               uuid=uuid,
          )
          if user is None:
               return UserNotFoundError
          return user
     
     
     async def get_user_steam_inventory(
          self, 
          async_session: AsyncSession,
          redis_session: RedisPool,
          uuid: str
     ) -> list[SteamItem] | AbstractResponse:
          user = await self.user_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"user:{uuid}",
               uuid=uuid
          )
          if user is None:
               return UserNotFoundError
          
          return await self.http_steam_client.get_steam_inventory(
               steamid=user.steam_id
          )
          
     
     
async def get_user_service() -> UserService:
     return UserService()