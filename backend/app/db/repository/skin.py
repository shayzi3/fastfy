
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel
from app.db.models import Skins

from .base import BaseRepository



class SkinRepository(BaseRepository[SkinModel, None]):
     model = Skins
     
     
     @classmethod
     async def search_skin(
          cls,
          session: AsyncSession,
          redis_session: RedisPool,
          query: str,
          offset: int,
     ) -> list[SkinModel] | None:
          pass