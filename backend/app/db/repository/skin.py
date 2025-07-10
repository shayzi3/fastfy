
from sqlalchemy import select
from app.db.session import AsyncSession, Session
from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel
from app.db.models import Skins
from app.schemas.enums import UpdateMode

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
     
     
     @classmethod
     async def read_all_task_update_price(
          cls,
          mode: UpdateMode
     ) -> list[Skins]:
          async with Session.session() as session:
               sttm = (
                    select(Skins).
                    where(Skins.update_mode == mode)
               )
               result = await session.execute(sttm)
               result = result.scalars().all()
          return result