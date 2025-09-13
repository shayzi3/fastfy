import json

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from app.db.session import AsyncSession
from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel, SkinsPage
from app.db.models import Skins

from .base import BaseRepository



class SkinRepository(
     BaseRepository[SkinModel, None]
):
     model = Skins
     
     
     @classmethod
     async def search_skin(
          cls,
          session: AsyncSession,
          redis_session: RedisPool,
          query: str,
          offset: int,
          limit: int
     ) -> SkinsPage[SkinModel]:
          value = await redis_session.get(f"{query}~{offset}~{limit}")
          if value:
               data = json.loads(value)
               return SkinsPage(
                    skins=[
                         SkinModel.model_validate(json.loads(model))
                         for model in data[:-1]
                    ],
                    current_page=offset,
                    pages=int(data[-1]),
                    skins_on_page=limit,
               ).serialize_pages()
               
          where_params = [
               Skins.name.ilike(f"%{query_part}%") 
               for query_part in query.split()
          ]
          
          sttm_skins = (
               select(Skins).
               where(*where_params).
               limit(limit).
               offset(offset)
          )
          sttm_count_skins = (
               select(func.count(Skins.name)).
               where(*where_params)
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
               dump_models = [
                    model.model_dump_json()
                    for model in pd_models
               ]
               dump_models.append(result_count)
               
               await redis_session.set(
                    name=f"{query}~{offset}~{limit}",
                    value=json.dumps(dump_models),
                    ex=120
               )
          return SkinsPage(
               pages=result_count,
               current_page=offset,
               skins=pd_models,
               skins_on_page=limit,
          ).serialize_pages()