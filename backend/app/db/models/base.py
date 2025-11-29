from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs



class Base(AsyncAttrs, DeclarativeBase):
     _table_name_and_orm_object: dict[str, "Base"] = {}
     
     @classmethod
     def table_names_with_orm_objects(cls) -> dict[str, "Base"]:
          """Метод возващает все имена таблиц и в качестве значения использует orm объекты"""
          if not cls._table_name_and_orm_object:
               mappers = cls.registry.mappers
               cls._table_name_and_orm_object = {mp.class_.__tablename__: mp.class_ for mp in mappers}
          return cls._table_name_and_orm_object