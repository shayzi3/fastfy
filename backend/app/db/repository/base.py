import json

from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

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
          result = None
          if (redis_key is not None) and (redis_session is not None):
               result = await redis_session.get(redis_key)
               if result is not None:
                    result = json.loads(result)
               
          if result is None:
               sttm = select(cls.model).filter_by(**read_args)
               if selectload is True:
                    sttm = sttm.options(selectinload(cls.model.selectinload()))
                    
               result = await session.execute(sttm)
               result = result.scalar()
               if result is None:
                    return None
          
          return_model = cls.model.pydantic_model
          if selectload is True:
               return_model = cls.model.pydantic_rel_model
          
          pydantic_model = return_model.model_validate(result, from_attributes=True)
          if (redis_key is not None) and (redis_session is not None):
               await redis_session.set(
                    name=redis_key,
                    value=pydantic_model.model_dump_json(),
                    ex=1000
               )
          return pydantic_model
     
     
     @classmethod
     async def create(
          cls,
          session: AsyncSession,
          data: list[dict] | dict = [], # many data for insert
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
          redis_session: RedisPool | None = None,
          delete_redis_values: list[str] = [],
          **update_args
     ) -> bool:
          sttm = (
               update(cls.model).
               filter_by(**where).
               values(**update_args).
               returning(cls.model.returning())
          )
          result = await session.execute(sttm)
          result = result.scalar()
          await session.commit()
          
          if (redis_session is not None) and (delete_redis_values):
               await redis_session.delete(*delete_redis_values)
          return True if result else False
               
               
     @classmethod
     async def delete(
          cls,
          session: AsyncSession,
          redis_session: RedisPool | None = None,
          delete_redis_values: list[str] = [],
          **delete_where
     ) -> bool:
          sttm = (
               delete(cls.model).
               filter_by(**delete_where).
               returning(cls.model.returning())
          )
          result = await session.execute(sttm)
          result = result.scalar()
          await session.commit()
          
          if (redis_session is not None) and (delete_redis_values):
               await redis_session.delete(*delete_redis_values)
          return True if result else False
               
               
               