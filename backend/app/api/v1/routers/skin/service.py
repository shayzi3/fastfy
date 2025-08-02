from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.infrastracture.https.steam import HttpSteamClient
from app.db.repository import SkinPriceHistoryRepository, SkinRepository
from app.responses.abstract import AbstractResponse
from app.responses import SkinNotFoundError, OffsetError
from app.schemas import SkinModel, SkinHistoryTimePartModel, SkinsPage




class SkinService:
     def __init__(self):
          self.skin_history_repository = SkinPriceHistoryRepository
          self.skin_repository = SkinRepository
          self.steam_client = HttpSteamClient()
          
          
     async def get_skin(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          skin_name: str
     ) -> SkinModel | AbstractResponse:
          result = await self.skin_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"skin:{skin_name}",
               name=skin_name
          )
          if result is None:
               return SkinNotFoundError
          return result
     
     
     async def search_skin(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          query: str,
          offset: int
     ) -> SkinsPage | AbstractResponse:
          if offset % 10 != 0:
               return OffsetError
          
          result = await self.skin_repository.search_skin(
               session=async_session,
               redis_session=redis_session,
               query=query,
               offset=offset
          )
          if not result.skins:
               return SkinNotFoundError
          return result
          
          
     async def skin_history(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          skin_name: str
     ) -> AbstractResponse | SkinHistoryTimePartModel:
          result = await self.skin_history_repository.filter_timestamp(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"skin_price_history:{skin_name}",
               skin_name=skin_name
          )
          if result is None:
               return SkinNotFoundError
          return result
          
          
          
async def get_skin_service() -> SkinService:
     return SkinService()