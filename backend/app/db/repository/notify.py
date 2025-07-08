import json

from sqlalchemy import select, update

from app.infrastracture.redis import RedisPool
from app.schemas import UserNotifyModel
from app.db.session import AsyncSession
from app.db.models.models import UsersNotify
from .base import BaseRepository



class NotifyRepository(BaseRepository[UserNotifyModel, None]):
     model = UsersNotify
     
     
     @classmethod
     async def read_all(
          cls,
          session: AsyncSession,
          redis_session: RedisPool | None = None,
          redis_key: str | None = None,
          **read_args
     ) -> list[UserNotifyModel]:
          if (redis_session is not None) and (redis_key is not None):
               result = await redis_session.get(redis_key)
               if result is not None:
                    data = json.loads(result)
                    return [
                         UserNotifyModel.model_validate(json.loads(model)) for model in data
                    ]
                    
          sttm = select(UsersNotify).filter_by(**read_args)
          result = await session.execute(sttm)
          result = result.scalars().all()
          
          models = [
               (
                    UserNotifyModel.
                    model_validate(model, from_attributes=True)
               ) for model in result
          ]
          if (redis_session is not None) and (redis_key is not None):
               await redis_session.set(
                    name=redis_key,
                    value=json.dumps(
                         [model.model_dump_json() for model in models]
                    ),
                    ex=500
               )
          return models
     
     
     @classmethod
     async def update_all(
          cls,
          session: AsyncSession,
          notify_ids: list[str],
          redis_session: RedisPool | None = None,
          delete_redis_values: list[str] = []
     ) -> None:
          sttm = (
               update(UsersNotify).
               filter(UsersNotify.notify_id.in_(notify_ids)).
               values(is_read=True)
          )
          await session.execute(sttm)
          await session.commit()
          
          if (redis_session is not None) and (delete_redis_values):
               await redis_session.delete(*delete_redis_values)