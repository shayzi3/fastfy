from typing import Any, Type, TypeVar, Generic, Iterable

from pydantic import BaseModel


DTO = TypeVar("DTO", bound=BaseModel)




class Mixin(Generic[DTO]):
     dto: Type[DTO]
     
     @classmethod
     def serialize_dto(cls, obj: Any, *, from_attributes: bool) -> DTO:
          return cls.dto.model_validate(obj, from_attributes=from_attributes)