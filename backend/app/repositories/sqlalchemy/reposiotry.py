import json

from typing import Any, Generic, TypeVar, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, insert, desc, func
from pydantic import BaseModel

from backend.app.infrastracture.cache.abc import Cache
from app.repositories.abc_repository import BaseRepository
from app.db.models import Base
from app.schemas.enums import OrderByModeEnum



DTO = TypeVar("BM", bound=BaseModel)    
SM = TypeVar("SM", bound=Base) # SQLAlchemy Model
     

   
class SQLAlchemyRepository(BaseRepository, Generic[DTO, SM]):
     model: SM = None
     
     def __init__(self, session: AsyncSession) -> None:
          self.session = session
          
          
     async def __query_builder(
          self,
          type_: Callable,
          where: dict[str, Any] | list[Any] = {},
          columns: list[str] = [],
          values: dict[str, Any] = {},
          selectinload: bool = False,
          returning: bool = False,
          order_by: str | None = None,
          order_by_mode: OrderByModeEnum = OrderByModeEnum.ASC,
          limit: int | None = None,
          offset: int | None = None,
          filter_by: bool = True
     ) -> Any:
          query = type_(self.model)
          if columns:
               query = type_(
                    *[
                         getattr(self.model, attr) 
                         for attr in columns if hasattr(self.model, attr)
                    ]
               )
          if values:
               query = query.values(**values)
               
          if where:
               if filter_by:
                    query = query.filter_by(**where)
               else:
                    query = query.where(*where)
               
          if selectinload:
               selectinload_values = self.model.selectinload()
               if selectinload_values:
                    query = query.options(*selectinload_values)

          if returning:
               returning_value = self.model.returning()
               if returning_value:
                    query = query.returning(returning_value)
                    
          if order_by:
               if hasattr(self.model, order_by):
                    oby_value = getattr(self.model, order_by)
                    if order_by_mode == OrderByModeEnum.DESC:
                         oby_value = desc(getattr(self.model, order_by))
                    query = query.order_by(oby_value)
          if limit:
               query = query.limit(limit)
          if offset:
               query = query.offset(offset)
               
          return query
          
          
          
     async def read(
          self,
          where: dict[str, Any] = {}, 
          cache: Cache | None = None,
          cache_key: str | None = None,
          selectinload: bool = False, 
          columns: list[str] = [],
          **kwargs
     ) -> DTO | Any:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    if columns:
                         return json.loads(data)
                    return self.model.serialize_dto(obj=data, from_attributes=False)
                         
          query = await self.__query_builder(
               type_=select,
               where=where,
               selectinload=selectinload,
               columns=columns
          )
          result = await self.session.execute(query)
          data = result.scalar()
          
          if not data:
               return None
          
          if not columns:
               data = self.model.serialize_dto(obj=data, from_attributes=True)
          
          if cache and cache_key:
               await cache.set(
                    name=cache_key, 
                    value=data.model_dump_json() 
                    if hasattr(data, "model_dump_json") else json.dumps(data)
               )
          return data

     
     async def read_all(
          self, 
          where: dict[str, Any] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
          selectinload: bool = False, 
          columns: list[str] = [],
          order_by: str | None = None,
          order_by_mode: OrderByModeEnum = OrderByModeEnum.ASC,
          **kwargs
     ) -> list[DTO]:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    loads_data = json.loads(data)
                    if columns: 
                         return loads_data
                    return [
                         self.model.serialize_dto(obj=json.loads(dump_model), from_attributes=False)
                         for dump_model in loads_data
                    ]
          
          query = await self.__query_builder(
               type_=select,
               where=where,
               columns=columns,
               selectinload=selectinload,
               order_by=order_by,
               order_by_mode=order_by_mode
          )
          result = await self.session.execute(query)
          data = result.scalars().all()
          
          if not data:
               return []
          
          if not columns:
               data = [
                    self.model.serialize_dto(obj=model, from_attributes=True) 
                    for model in data
               ]
               
          if cache and cache_key:
               if hasattr(data[0], "model_dump_json"):
                    data = [model.model_dump_json() for model in data]
               await cache.set(name=cache_key, value=json.dumps(data))
          return data
                    
          
     async def create(
          self, 
          values: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: bool = False,
          **kwargs
     ) -> Any:
          query = await self.__query_builder(
               type_=insert,
               returning=returning,
               values=values
          )
          result = await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
          
          if returning is True:
               return result.scalar()
          
          
     async def create_many(
          self,
          values: list[dict[str, Any]],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          **kwargs
     ) -> None:
          query = await self.__query_builder(
               type_=insert,
               values=values
          )
          await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
     
     
     async def update(
          self, 
          values: dict[str, Any],
          where: dict[str, Any],
          cache: Cache | None = None,
          cache_keys: list[str] = [],
          returning: bool = False, 
          **kwargs
     ) -> Any:
          query = await self.__query_builder(
               type_=update,
               values=values,
               where=where,
               returning=returning
          )
          result = await self.session.execute(query)
          
          if cache and cache_keys:
               await cache.delete(*cache_keys)
               
          if returning is True:
               return result.scalar()
          
          
     async def delete(
          self, 
          where: dict[str, Any],
          cache: Cache | None = None,
          cache_key: list[str] = [],
          returning: bool = False, 
          **kwargs
     ) -> Any:
          query = await self.__query_builder(
               type_=delete,
               where=where,
               returning=returning
          )
          result = await self.session.execute(query)
          
          if cache and cache_key:
               await cache.delete(*cache_key)
               
          if returning is True:
               return result.scalar()
          
          
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
          order_by_mode: str = "",
          columns: list[str] = [],
          **kwargs
     ) -> tuple[list[DTO | tuple[Any]], int]:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    loads_data = json.loads(data)
                    if columns:
                         return loads_data[:-1], int(loads_data[-1])
                    return [self.model.serialize_dto(dump_dto) for dump_dto in loads_data[:-1]], int(loads_data[-1])
          
          where_values = []
          if query:
               where_values = [
                    self.model.paginate_query_column().ilike(f"%{query_part}%")
                    for query_part in query.split()
               ]
          if where:
               where_values.extend(
                    [
                         getattr(self.model, key) == value for key, value in where.items() 
                         if hasattr(self.model, key)
                    ]
               )
               
          query_items = await self.__query_builder(
               type_=select,
               where=where_values,
               columns=columns,
               selectinload=selectinload,
               order_by=order_by,
               order_by_mode=order_by_mode,
               limit=limit,
               offset=offset,
               filter_by=False
          )
          query_count_items = (
               select(func.count(self.model.returning())).
               where(*where_values)
          )
          items = await self.session.execute(query_items)
          result_items = items.scalars().all()
          
          count = await self.session.execute(query_count_items)
          result_count = count.scalar()
          
          if not columns:
               items = [
                    self.model.serialize_dto(model, from_attributes=True)
                    for model in result_items
               ]
               
          if cache and cache_key:
               if not columns:
                    items = [dto.model_dump_json() for dto in items]
                    
               items.append(result_count)
               await cache.set(
                    key=cache_key,
                    value=json.dumps(items),
                    ex=80
               )
          return items, result_count          
          
          
     
     
     