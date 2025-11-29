from typing import Type, TypeVar, Generic

from pydantic import BaseModel

from app.db.models import Base

     


DTO = TypeVar("DTO", bound=BaseModel)



class Mixin(Generic[DTO]):
     dto: Type[DTO]
     
     _table_with_orm: dict[str, Base] = {}
     
     @classmethod
     def serialize_dto(cls, sqm_instance: Base) -> DTO:
          """Сериализация из SQLAlchemy модели в Pydantic"""
          return cls.dto.model_construct(**getattr(sqm_instance, "__dict__", {}))