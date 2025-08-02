import json

from sqlalchemy import select, func
from app.db.session import AsyncSession, Session
from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel, SkinsPage
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
          offset: int
     ) -> SkinsPage:
          value = await redis_session.get(f"{query}~{offset}")
          if value:
               parts = value.split("~~")
               return SkinsPage(
                    pages=int(parts[-1]),
                    current_page=offset,
                    skins=parts[0]
               )
               
          sttm_skins = (
               select(Skins).
               where(Skins.name.ilike(f"%{query}%")).
               limit(10).
               offset(offset)
          )
          sttm_count_skins = (
               select(func.count(Skins.name)).
               where(Skins.name.ilike(f"%{query}%"))
          )
          result_skins = await session.execute(sttm_skins)
          result_skins = result_skins.scalars().all()
          
          result_count = await session.execute(sttm_count_skins)
          result_count = result_count.scalar()
          
          pd_models = [
               SkinModel.model_validate(model, from_attributes=True) 
               for model in result_skins
          ]
          if pd_models:
               await redis_session.set(
                    name=f"{query}~{offset}",
                    value=json.dumps(
                         [pd_model.model_dump_json() for pd_model in pd_models]
                    ) + f"~~{result_count}",
                    ex=30
               )
          return SkinsPage(
               pages=result_count,
               current_page=offset,
               skins=pd_models
          )
     
     
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