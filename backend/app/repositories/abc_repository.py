from typing import Any, TypeVar, Generic, Protocol

from pydantic import BaseModel

from app.schemas.enums import OrderByModeEnum
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_condition import BaseWhereCondition


DTO = TypeVar("DTO", bound=BaseModel)
ESSENCE = TypeVar("ESSENSE")


class BaseRepository(Protocol, Generic[DTO, ESSENCE]):
     model: ESSENCE
     
     def __init__(self, session: Any) -> None: 
          self.session = session
          

     async def read(
          self, 
          cache: Cache | None = None,
          cache_key: str | None = None,
          relationship_columns: list[str] = [],
          joinedload_relship_columns: list[str] = [],
          where: dict[str, list[BaseWhereCondition]] = {},
          columns: list[str] = [],
     ) -> DTO | list[tuple[Any]] | None:
          ...
     
     
     async def read_many(
          self, 
          cache: Cache | None = None,
          cache_key: str | None = None,
          relationship_columns: list[str] = [],
          joinedload_relship_columns: list[str] = [],
          where: dict[str, list[BaseWhereCondition]] = {},
          columns: list[str] = [],
          order_by: dict[str, list[tuple[str, OrderByModeEnum]]] = {},
          limit: int | None = None,
          offset: int | None = None,
          count: bool = False
     ) -> tuple[list[DTO], int]:
          ...
     
     
     async def create(
          self,
          values: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None,
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
          where: dict[str, list[BaseWhereCondition]], 
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None, 
     ) -> Any:
          ...
          
     async def delete(
          self, 
          where: dict[str, list[BaseWhereCondition]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None, 
     ) -> Any:
          ...