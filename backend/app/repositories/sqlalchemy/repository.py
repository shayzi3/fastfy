import json

from typing import Any, Generic, TypeVar, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert
from pydantic import BaseModel

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_repository import BaseRepository
from app.repositories.sqlalchemy.condition import SQLAlchemyWhereCondition
from app.db.models import Base
from app.schemas.enums import OrderByModeEnum
from .query_build import QueryBuilder


DTO = TypeVar("BM", bound=BaseModel)    
SM = TypeVar("SM", bound=Base) # SQLAlchemy Model
     

   
class SQLAlchemyRepository(BaseRepository, Generic[DTO, SM]):
     model: SM = None
     
     def __init__(self, session: AsyncSession) -> None:
          self.session = session
          self.__query_builder = QueryBuilder
          
          
     async def read(
          self,
          cache: Cache | None = None,
          cache_key: str | None = None,
          relationship_columns: list[str] = [],
          joinedload_relship_columns: list[str] = [],
          where: dict[str, list[SQLAlchemyWhereCondition]] = {},
          columns: list[str] = [],
          **kwargs
     ) -> DTO | list[tuple[Any]] | None:
          if cache and cache_key:
               data = await cache.get(key=cache_key)
               if data:
                    load_data = json.loads(data)
                    if columns:
                         return load_data
                    return self.model.serialize_dto(load_data)
                      
          query_build = (
               self.__query_builder(
                    query_type=select,
                    model=self.model,
                    columns=columns,
               ).
               joinedload(joinedload_relship_columns).
               join(relationship_columns).
               where(where)
          )
          result = await self.session.execute(query_build.query)
          data = result.scalar() if not columns else result.all()
          
          if not data:
               return None
          
          if not columns:
               data = self.model.serialize_dto(obj=data)
          
          if cache and cache_key:
               await cache.set(
                    key=cache_key, 
                    value=json.dumps(data)
                    if columns else data.model_dump_json(),
                    ex=60
               )
          return data

     
     async def read_many(
          self, 
          cache: Cache | None = None,
          cache_key: str | None = None,
          relationship_columns: list[str] = [],
          joinedload_relship_columns: list[str] = [],
          where: dict[str, list[SQLAlchemyWhereCondition]] = {},
          columns: list[str] = [],
          order_by: dict[str, list[tuple[str, OrderByModeEnum]]] = {},
          limit: int | None = None,
          offset: int | None = None,
          count: bool = False,
          **kwargs
     ) -> tuple[list[DTO], int]:
          if cache and cache_key:
               data = await cache.get(key=cache_key)
               if data:
                    loads_data = json.loads(data)
                    payload, count_data = json.loads(loads_data["payload"]), loads_data["count"]
                    if columns: 
                         return (payload, count_data)
                    return (
                         [
                              self.model.serialize_dto(obj=json.loads(dump_model))
                              for dump_model in payload
                         ],
                         count_data
                    )
          
          query_build_data = (
               self.__query_builder(
                    query_type=select,
                    model=self.model,
                    columns=columns,
               ).
               join(relationship_columns).
               where(where).
               order_by(order_by).
               limit(limit).
               offset(offset).
               joinedload(joinedload_relship_columns)
          )
          result_data = await self.session.execute(query_build_data.query)
          if joinedload_relship_columns:
               data = result_data.unique().all()
          else:
               data = result_data.all()
               
          count_data = 0
          if count is True:
               query_build_count = (
                    self.__query_builder(
                         query_type=select,
                         count=True,
                         model=self.model
                    ).join(relationship_columns).where(where)
               )
               result_count = await self.session.execute(query_build_count.query)
               count_data = result_count.scalar()
               
          if not data:
               return ([], 0)
          
          if not columns:
               data = [
                    self.model.serialize_dto(obj=model[0]) 
                    for model in data
               ]
               
          if cache and cache_key:
               redis_save_data = data.copy()
               if not columns:
                    redis_save_data = [model.model_dump_json() for model in data]
                    
               cache_data = {
                    "payload": json.dumps(redis_save_data),
                    "count": count_data
               }
               await cache.set(key=cache_key, value=json.dumps(cache_data), ex=60)
          return (data, count_data)
                    
          
     async def create(
          self,
          values: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None,
          **kwargs
     ) -> Any:
          query_build = (
               self.__query_builder(
                    query_type=insert,
                    model=self.model
               ).values(values).returning(returning)
          )
          result = await self.session.execute(query_build.query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
          
          if returning:
               return result.scalar()
          
          
     async def create_many(
          self,
          values: list[dict[str, Any]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          **kwargs
     ) -> None:
          query_build = (
               self.__query_builder(
                    query_type=insert,
                    model=self.model
               ).values(values)
          )
          await self.session.execute(query_build.query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
     
     
     async def update(
          self, 
          values: dict[str, Any],
          where: dict[str, list[SQLAlchemyWhereCondition]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None, 
          **kwargs
     ) -> Any:
          query_build = (
               self.__query_builder(
                    query_type=update,
                    model=self.model
               ).values(values).where(where).returning(returning)
          )
          result = await self.session.execute(query_build.query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
               
          if returning:
               return result.scalar()
          
          
     async def delete(
          self, 
          where: dict[str, list[SQLAlchemyWhereCondition]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None,
          **kwargs
     ) -> Any:
          query_build = (
               self.__query_builder(
                    query_type=select,
                    model=self.model
               ).where(where).returning(returning)
          )
          result = await self.session.execute(query_build.query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
               
          if returning:
               return result.scalar()