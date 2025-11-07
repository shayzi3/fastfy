from typing import Any, Type, TypeVar, Generic, Iterable

from pydantic import BaseModel


DTO = TypeVar("DTO", bound=BaseModel)




class Mixin(Generic[DTO]):
     dto: Type[DTO]
     
     @classmethod
     def serialize_dto(cls, from_attributes: bool, obj: Any) -> DTO:
          return cls.dto.model_validate(
               obj=obj, 
               from_attributes=True if from_attributes else False
          )