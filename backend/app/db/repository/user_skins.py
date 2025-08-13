import json

from sqlalchemy import select, func

from app.db.session import AsyncSession
from app.infrastracture.redis import RedisPool
from app.schemas import UserSkinModel, UserSkinRelModel, SkinsPage
from app.db.models import UsersSkins

from .base import BaseRepository



class UserSkinRepository(
     BaseRepository[UserSkinModel, UserSkinRelModel]
):
     model = UsersSkins
     
     
     @classmethod
     async def read_paginate(
          cls,
          session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          offset: int,
          limit: int
     ) -> SkinsPage:
          value = await redis_session.get(f"user_portfolio:{user_uuid}~{offset}~{limit}")
          if value is not None:
               models = json.loads(value)
               return SkinsPage(
                    pages=int(models[-1]),
                    current_page=offset,
                    skins=models[:-1],
                    skin_model_obj=UserSkinRelModel,
                    skins_on_page=limit
               )
               
          sttm_models = (
               select(UsersSkins).
               filter_by(user_uuid=user_uuid).
               limit(limit).
               offset(offset).
               options(*UsersSkins.selectinload())
          )
          sttm_pages = (
               select(func.count(UsersSkins.skin_name)).
               filter_by(user_uuid=user_uuid)
          )
          result_models = await session.execute(sttm_models)
          result_models = result_models.scalars().all()
          
          result_pages = await session.execute(sttm_pages)
          result_pages = result_pages.scalar()
          
          models = [
               UserSkinRelModel.model_validate(model, from_attributes=True)
               for model in result_models
          ]
          if models:
               dump_models = [model.model_dump_json() for model in models]
               dump_models.append(result_pages)
               
               await redis_session.set(
                    name=f"user_portfolio:{user_uuid}~{offset}~{limit}",
                    value=json.dumps(dump_models),
                    ex=120
               )
          return SkinsPage(
               pages=result_pages,
               current_page=offset,
               skins=models,
               skin_model_obj=UserSkinRelModel,
               skins_on_page=limit
          )
     
     
     
          
          