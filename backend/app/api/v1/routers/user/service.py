from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.db.repository import UserRepository
from app.schemas import UserModel, SkinsPage, SteamItem
from app.responses import UserNotFoundError, UserUpdateSuccess, OffsetError, isresponse, SkinNotFoundError
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
          user_uuid: str
     ) -> UserModel | AbstractResponse:
          user = await self.user_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"user:{user_uuid}",
               uuid=user_uuid
          )
          if user is None:
               return UserNotFoundError
          return user
     
     
     async def patch_skin_percent_user(
          self,
          async_session: AsyncSession,
          user_uuid: str,
          skin_percent: int
     ) -> AbstractResponse:
          user_update = await self.user_repository.update(
               session=async_session,
               where={"uuid": user_uuid},
               skin_percent=skin_percent
          )
          if user_update is True:
               return UserUpdateSuccess
          return UserNotFoundError
     
     
     async def get_user_steam_inventory(
          self, 
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          offset: int,
          limit: int
     ) -> SkinsPage | AbstractResponse:
          if offset % limit != 0:
               return OffsetError
          
          user = await self.user_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"user:{user_uuid}",
               uuid=user_uuid
          )
          if user is None:
               return UserNotFoundError

          result = await self.http_steam_client.get_steam_inventory(
               steamid=user.steam_id,
               redis_session=redis_session,
               offset=offset,
               limit=limit,
          )
          if isresponse(result):
               return result
          
          if not result.skins:
               return SkinNotFoundError
          return result
          
     
     
async def get_user_service() -> UserService:
     return UserService()