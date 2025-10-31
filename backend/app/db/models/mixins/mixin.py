from typing import Any, Type, TypeVar, Generic, Iterable, Literal

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
          
     @classmethod
     def returning(cls) -> None | Any:
          return None
     
     @classmethod
     def order_by(cls) -> None | Any:
          return None
     
     @classmethod
     def selectinload(cls) -> Iterable:
          return []
     
     @classmethod
     def paginate_query_column(cls):
          return None