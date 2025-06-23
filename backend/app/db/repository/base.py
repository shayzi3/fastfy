from typing import Any, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy import insert, delete, update, select
from sqlalchemy.orm import selectinload

from ..session import Session


PYDANTIC_MODEL = TypeVar("MODEL", bound=BaseModel)
PYDANTIC_MODELRel = TypeVar("MODELRel", bound=BaseModel)



class BaseRepository(Generic[PYDANTIC_MODEL, PYDANTIC_MODELRel]):
     model = None
     
     
     @classmethod
     async def read(
          cls,
          selectload: bool = False,
          **read_args
     ) -> PYDANTIC_MODEL | PYDANTIC_MODELRel | None:
          sttm = select(cls.model).filter_by(**read_args)
          if selectload is True:
               sttm = sttm.options(selectinload(cls.model.selectinload()))
               
          async with Session.session() as async_session:
               result = await async_session.execute(sttm)
               result_scalar = result.scalar()
               
               if result_scalar is None:
                    return None
               
          return_model = cls.model.pydantic_model
          if selectload is True:
               return_model = cls.model.pydantic_rel_model
          return return_model.model_validate(result_scalar, from_attributes=True)
     
     
     @classmethod
     async def create(
          cls,
          **insert_args
     ) -> Any:
          async with Session.session() as async_session:
               sttm = (
                    insert(cls.model).
                    values(**insert_args).
                    returning(cls.model.returning())
               )
               result = await async_session.execute(sttm)
               result = result.scalar()
               await async_session.commit()
          return result
               
               
     @classmethod
     async def update(
          cls,
          where: dict[str, Any],
          **update_args
     ) -> bool:
          async with Session.session() as async_session:
               sttm = (
                    update(cls.model).
                    filter_by(**where).
                    values(**update_args).
                    returning(cls.model.returning())
               )
               result = await async_session.execute(sttm)
               result = result.scalar()
               await async_session.commit()
          return True if result else False
               
               
     @classmethod
     async def delete(
          cls,
          **delete_where
     ) -> bool:
          async with Session.session() as async_session:
               sttm = (
                    delete(cls.model).
                    filter_by(**delete_where).
                    returning(cls.model.returning())
               )
               result = await async_session.execute(sttm)
               result = result.scalar()
               await async_session.commit()
          return True if result else False
               
               
               