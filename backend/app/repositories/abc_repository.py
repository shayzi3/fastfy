from typing import Any, TypeVar, Generic, Protocol, Type, Literal

from pydantic import BaseModel

from app.schemas.enums import OrderByModeEnum
from app.schemas import SkinsPage
from app.infrastracture.cache.abc import Cache


DTO = TypeVar("DTO", bound=BaseModel)
ESSENCE = TypeVar("ESSENSE")


class BaseRepository(Protocol, Generic[DTO, ESSENCE]):
     model: ESSENCE
     
     def __init__(self, session: Any) -> None: 
          self.session = session
          

     async def read(
          self, 
          where: dict[str, Any] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
          selectinload: bool = False, 
          columns: list[str] = [],
     ) -> DTO | None:
          ...
     
     
     async def read_all(
          self, 
          where: dict[str, Any] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
          selectinload: bool = False, 
          columns: list[str] = [],
          order_by: str | None = None,
          order_by_mode: OrderByModeEnum = OrderByModeEnum.ASC,
     ) -> list[DTO]:
          ...
     
     
     async def create(
          self, 
          values: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: bool = False,
     ) -> Any:
          ...
     
     
     async def create_many(
          self, 
          values: list[dict[str, Any]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
     ) -> None:
          ...

     
     async def update(
          self, 
          values: dict[str, Any],
          where: dict[str, Any], 
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: bool = False, 
     ) -> Any:
          ...
     
     
     async def delete(
          self, 
          where: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: bool = False, 
     ) -> Any:
          ...
          
          
     async def paginate(
          self,
          limit: int,
          offset: int,
          query: str = "",
          where: dict[str, Any] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
          selectinload: bool = False,
          order_by: str = "",
          columns: list[str] = [],
          order_by_mode: str = "",
     ) -> tuple[list[DTO | tuple[Any]], int]:
          ...