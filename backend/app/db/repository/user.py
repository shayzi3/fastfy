from typing import Any
from sqlalchemy import insert, update, select

from app.db.session import Session
from app.schemas import UserModel
from app.db.models import Users



class UserRepository:
     model = Users
     
     
     @classmethod
     async def read(cls, **read_args) -> UserModel | None:
          async with Session.session() as async_session:
               sttm = select(cls.model).filter_by(**read_args)
               result = await async_session.execute(sttm)
               result = result.scalar()
               
               if result is None:
                    return None
               return cls.model.pydantic_model.model_validate(result.dump())
     
     
     @classmethod
     async def insert(cls, **insert_args) -> None:
          async with Session.session() as async_session:
               sttm = insert(cls.model).values(**insert_args).returning()
               await async_session.execute(sttm)
               await async_session.commit()
               
          
          
     @classmethod
     async def update(cls, where: dict[str, Any], **update_args) -> None:
          async with Session.session() as async_session:
               sttm = (
                    update(cls.model).
                    filter_by(**where).
                    values(**update_args)
               )
               await async_session.execute(sttm)
               await async_session.commit()
     