import json

from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSession
from app.infrastracture.redis import RedisPool



PYDANTIC_MODEL = TypeVar("PYDANTIC_MODEL", bound=BaseModel)
PYDANTIC_MODELRel = TypeVar("PYDANTIC_MODELRel", bound=BaseModel)



class BaseRepository(Generic[PYDANTIC_MODEL, PYDANTIC_MODELRel]):
     model = None
     
     
     @classmethod
     async def read(
          cls,
          session: AsyncSession,
          redis_session: RedisPool | None = None,
          selectload: bool = False,
          redis_key: str | None = None,
          **read_args
     ) -> PYDANTIC_MODEL | PYDANTIC_MODELRel | None:
          pydantic_model = cls.model.pydantic_model
          if selectload is True:
               pydantic_model = cls.model.pydantic_rel_model
          
          if (redis_key is not None) and (redis_session is not None):
               result = await redis_session.get(redis_key)
               if result is not None:
                    return pydantic_model.model_validate(
                         json.loads(result)
                    )
               
          sttm = select(cls.model).filter_by(**read_args)
          if selectload is True:
               sttm = sttm.options(*cls.model.selectinload())
                    
          result = await session.execute(sttm)
          result = result.scalar()
          if result is None:
               return None
          
          pydantic_model = pydantic_model.model_validate(result, from_attributes=True)
          if (redis_key is not None) and (redis_session is not None):
               await redis_session.set(
                    name=redis_key,
                    value=pydantic_model.model_dump_json(),
                    ex=60
               )
          return pydantic_model
     
     
     @classmethod
     async def read_all(
          cls,
          session: AsyncSession,
          redis_session: RedisPool | None = None,
          selectload: bool = False,
          redis_key: str | None = None,
          **read_all_args
     ) -> list[PYDANTIC_MODEL] | list[PYDANTIC_MODELRel]:
          pydantic_model = cls.model.pydantic_model
          if selectload is True:
               pydantic_model = cls.model.pydantic_rel_model
          
          if (redis_key is not None) and (redis_session is not None):
               value = await redis_session.get(redis_key)
               if value is not None:
                    values = json.loads(value)
                    return [
                         pydantic_model.model_validate(json.loads(obj)) for obj in values
                    ]
          sttm = (
               select(cls.model).
               order_by(cls.model.order_by())
          )
          if read_all_args:
               sttm = sttm.filter_by(**read_all_args)
               
          if selectload is True:
               sttm = sttm.options(*cls.model.selectinload())
               
          result = await session.execute(sttm)
          result = result.scalars().all()
               
          models = [
               pydantic_model.model_validate(obj, from_attributes=True)
               for obj in result
          ]
          if models:
               if (redis_key is not None) and (redis_session is not None):
                    await redis_session.set(
                         name=redis_key,
                         value=json.dumps(
                              [pymodel.model_dump_json() for pymodel in models]
                         ),
                         ex=60
                    )
          return models
     
     
     @classmethod
     async def create(
          cls,
          session: AsyncSession,
          data: list[dict] = [], # many data for insert
          **insert_args
     ) -> Any:
          if not data:
               sttm = (
                    insert(cls.model).
                    values(**insert_args).
                    returning(cls.model.returning())
               )
          else:
               sttm = insert(cls.model).values(data)
               
          if not data:
               result = await session.execute(sttm)
               await session.commit()
               return result.scalar()
          else:
               await session.execute(sttm)
               await session.commit()
                    
               
     @classmethod
     async def update(
          cls,
          session: AsyncSession,
          where: dict[str, Any],
          **update_args
     ) -> Any:
          sttm = (
               update(cls.model).
               filter_by(**where).
               values(**update_args).
               returning(cls.model.returning())
          )
          result = await session.execute(sttm)
          await session.commit()
          
          return result.scalar()
     
     
     @classmethod
     async def delete(
          cls,
          session: AsyncSession,
          **delete_where
     ) -> Any:
          sttm = (
               delete(cls.model).
               filter_by(**delete_where).
               returning(cls.model.returning())
          )
          result = await session.execute(sttm)
          await session.commit()
          
          return result.scalar()   
               
               