import json

from typing import Any, Generic, TypeVar, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import (
     select, 
     update, 
     delete, 
     insert, 
     func, 
     inspect, 
     asc, 
     desc
)
from pydantic import BaseModel

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_repository import BaseRepository
from app.repositories.abc_condition import BaseWhereCondition
from app.db.models import Base
from app.schemas.enums import OrderByModeEnum



DTO = TypeVar("BM", bound=BaseModel)    
SM = TypeVar("SM", bound=Base) # SQLAlchemy Model
     

   
class SQLAlchemyRepository(BaseRepository, Generic[DTO, SM]):
     model: SM = None
     
     def __init__(self, session: AsyncSession) -> None:
          self.session = session
          
          
     async def _query_builder(
          self,
          type_: Callable,
          relationship_columns: list[str] = [],
          where: dict[str, list[BaseWhereCondition]] = {},
          columns: list[str] = [],
          values: dict[str, Any] = {},
          returning: bool = False,
          order_by: dict[str, list[tuple[str, OrderByModeEnum]]] | None = None,
          limit: int | None = None,
          offset: int | None = None,
          joinedload_relship_columns: list[str] = [],
          count: bool = False
     ) -> Any:
          query = type_(self.model)
          
          if count is True:
               query = type_(func.count(self.model))
               
          if columns:
               columns_objects = []
               for attr in columns:
                    if isinstance(attr, str):
                         columns_objects.append(getattr(self.model, attr))
                    else:
                         columns_objects.append(attr)
                         
               query = type_(*columns_objects)
               
          if relationship_columns:
               query = query.join(
                    *[getattr(self.model, column) for column in relationship_columns]
               )
               
          if joinedload_relship_columns:
               query = query.options(
                    *[joinedload(getattr(self.model, column)) for column in joinedload_relship_columns]
               )
          
          if values:
               query = query.values(**values)
               
          if where:
               where_default = []
               for condition in where.get("default", []):
                    value = condition(model=self.model)
                    if isinstance(value, list | tuple):
                        where_default.extend(value)
                    else:
                        where_default.append(value)

               where_relationship_columns = []
               model_relationships = inspect(self.model).relationships
               
               for relationship_column, conditions in where.items():
                    if relationship_column != "default":
                         relationship_obj = model_relationships.get(relationship_column, None)
                         if relationship_obj:
                              relationship_class = relationship_obj.mapper.class_

                              for condition in conditions:
                                   value = condition(model=relationship_class)
                                   if isinstance(value, list | tuple):
                                       where_relationship_columns.extend(value)
                                   else:
                                       where_relationship_columns.append(value)
                                  
               query = query.where(*where_default, *where_relationship_columns)
          
          if order_by:
               order_by_values = []
               for attr, columns_modes in order_by.items():
                    for column_mode in columns_modes:
                         mode = asc if column_mode[1] == OrderByModeEnum.ASC else desc
                         
                         if attr == "default":
                              order_by_values.append(mode(getattr(self.model, attr)))
                         else:
                              relationship_obj = model_relationships.get(attr, None)
                              if relationship_obj:
                                   relationship_class = relationship_obj.mapper.class_
                                   order_by_values.append(mode(getattr(relationship_class, column_mode[0])))
                         
               query = query.order_by(*order_by_values)
               
          if returning:
               query = query.returning(getattr(self.model, returning))
               
          if limit:
               query = query.limit(limit)
               
          if offset:
               query = query.offset(offset)
          return query
          
          
          
     async def read(
          self,
          cache: Cache | None = None,
          cache_key: str | None = None,
          relationship_columns: list[str] = [],
          joinedload_relship_columns: list[str] = [],
          where: dict[str, list[BaseWhereCondition]] = {},
          columns: list[str] = [],
          **kwargs
     ) -> DTO | list[tuple[Any]] | None:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    if columns:
                         return json.loads(data)
                    return self.model.serialize_dto(obj=data, from_attributes=False)
                         
          query = await self._query_builder(
               type_=select,
               where=where,
               columns=columns,
               relationship_columns=relationship_columns,
               joinedload_relship_columns=joinedload_relship_columns
          )
          result = await self.session.execute(query)
          data = result.scalar() if not columns else result.all()
          
          if not data:
               return None
          
          if not columns:
               data = self.model.serialize_dto(obj=data, from_attributes=True)
          
          if cache and cache_key:
               await cache.set(
                    name=cache_key, 
                    value=json.dumps(data)
                    if columns else data.model_dump_json() 
               )
          return data

     
     async def read_all(
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
          count: bool = False,
          **kwargs
     ) -> tuple[list[DTO], int | None]:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    loads_data = json.loads(data)
                    if columns: 
                         return loads_data
                    return (
                         [
                              self.model.serialize_dto(obj=json.loads(dump_model), from_attributes=False)
                              for dump_model in loads_data[:-1]
                         ],
                         int(loads_data[-1]) if loads_data[-1] else None
                    )
          
          query_data = await self._query_builder(
               type_=select,
               where=where,
               columns=columns,
               order_by=order_by,
               relationship_columns=relationship_columns,
               joinedload_relship_columns=joinedload_relship_columns,
               limit=limit,
               offset=offset
          )
          result_data = await self.session.execute(query_data)
          data = result_data.all()
          
          count_data = None
          if count is True:
               query_count = await self._query_builder(
                    type_=select,
                    count=True,
                    where=where,
                    relationship_columns=relationship_columns
               )
               result_count = await self.session.execute(query_count)
               count_data = result_count.scalar()
               
          if not data:
               return ([], None)
          
          if not columns:
               data = [
                    self.model.serialize_dto(obj=model, from_attributes=True) 
                    for model in data
               ]
               
          if cache and cache_key:
               if not columns:
                    data = [model.model_dump_json() for model in data]
               
               data.append(count_data)
               await cache.set(name=cache_key, value=json.dumps(data))
          return (data, count_data)
                    
          
     async def create(
          self,
          values: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None,
          **kwargs
     ) -> Any:
          query = await self._query_builder(
               type_=insert,
               returning=returning,
               values=values
          )
          result = await self.session.execute(query)
          
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
          query = await self._query_builder(
               type_=insert,
               values=values
          )
          await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
     
     
     async def update(
          self, 
          values: dict[str, Any],
          where: dict[str, list[BaseWhereCondition]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None, 
          **kwargs
     ) -> Any:
          query = await self._query_builder(
               type_=update,
               values=values,
               where=where,
               returning=returning
          )
          result = await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
               
          if returning:
               return result.scalar()
          
          
     async def delete(
          self, 
          where: dict[str, list[BaseWhereCondition]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: str | None = None,
          **kwargs
     ) -> Any:
          query = await self._query_builder(
               type_=delete,
               where=where,
               returning=returning
          )
          result = await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
               
          if returning:
               return result.scalar()