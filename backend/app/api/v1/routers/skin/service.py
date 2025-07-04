from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.infrastracture.https.steam import HttpSteamClient
from app.db.repository import SkinPriceHistoryRepository, SkinRepository
from app.responses.abstract import AbstractResponse
from app.responses import SkinNotFoundError
from app.schemas import SkinModel, SkinHistoryTimePartModel




class SkinService:
     def __init__(self):
          self.skin_history_repository = SkinPriceHistoryRepository
          self.skin_repository = SkinRepository
          self.steam_client = HttpSteamClient()
          
          
     async def get_skin(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          skin_id: int | None = None,
          skin_name: str | None = None
     ) -> SkinModel | AbstractResponse:
          arguments = {
               "id": skin_id
          } if skin_id is not None else {
               "name": skin_name
          }
          result = await self.skin_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"skin:{list(arguments.values())[0]}",
               **arguments
          )
          if result is None:
               return SkinNotFoundError
          return result
     
     
     async def search_skin(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          query: str,
          steam: bool,
          offset: int
     ) -> list[SkinModel] | list[dict[str, Any]] | AbstractResponse:
          if steam is False:
               result = await self.skin_repository.search_skin(
                    session=async_session,
                    redis_session=redis_session,
                    query=query,
                    offset=offset,
               )
               if result is None:
                    return SkinNotFoundError
               return result
          else:
               result = await self.steam_client.search_steam_skins(
                    redis_session=redis_session,
                    query=query,
                    offset=offset
               )
               return result
          
          
     async def skin_history(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          skin_id: str | None = None,
          skin_name: str | None = None
     ) -> AbstractResponse | SkinHistoryTimePartModel:
          arguments = {
               "skin_id": skin_id
          } if skin_id is not None else {
               "skin_name": skin_name
          }
          result = await self.skin_history_repository.filter_timestamp(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"skin_price_history:{list(arguments.values())[0]}",
               **arguments
          )
          return result
          
          
          
async def get_skin_service() -> SkinService:
     return SkinService()