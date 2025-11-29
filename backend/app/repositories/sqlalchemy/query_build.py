from typing_extensions import Self, Any, TypeVar, Callable
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from sqlalchemy.sql.dml import Insert, Update, Delete, Select
from sqlalchemy.orm._orm_constructors import _RelationshipDeclared

from app.db.models import Base
from app.repositories.sqlalchemy.condition import SQLAlchemyWhereCondition, SQLAlchemyOrderByCondition


SM = TypeVar("SM", bound=Base)

class QueryBuilder:
     """
          Этот класс используется для постройки query запросов SQLAlchemy.
          Примеры классов взяты из app/db/models/models.py
     """
     
     __slots__ = (
          "_query",
          "_query_type", 
          "_model",
          "_orm_objects"
     )
     
     def __init__(
          self,
          query_type: Callable,
          model: SM
     ):
          """
               Args:
                    query_type (Callable): тип запроса. select, insert, update, delete
                    model (SM): модель алхимии
               
               _orm_objects хранит словарь, где ключ - название таблицы, значение - orm объект этой таблицы
z          """
          self._model = model
          self._query_type = query_type
          self._orm_objects = model.table_names_with_orm_objects()
          self._query = query_type(model)
               
     def columns(self, columns: dict[str, list[str]]) -> Self:
          """Поля, которые нужно вернуть при select запросе
          
               Производится итерация по всем переданным columns, далее происходит
               получение orm объекта, после итерируясь по колонкам этой таблицы 
               в mapped_columns уходят атрибуты orm объекта.

          Args:
               columns (dict[str, list[str]]): 
                    Ключ - название таблицы в бд.
                    Значение - колонки, которые следует вернуть при запросе
          Raises:
               TypeError: columns only for select
               ValueError: column not exists at table
               ValueError: table not exists
               
          Returns:
              Self
          """
          if isinstance(self._query, Select):
               raise TypeError("columns only for select")
          
          mapped_columns = []
          for table_name, columns_ in columns.items():
               orm_obj = self._orm_objects.get(table_name)
               if orm_obj is None:
                    raise ValueError(f"table {table_name} not exists")
               
               mapped_objects = []
               for c in columns_:
                    if hasattr(orm_obj, c):
                         mapped_objects.append(getattr(orm_obj, c))
                    else:
                         raise ValueError(f"column {c} not exists at table {table_name}")
               
               if mapped_objects:
                    mapped_columns.extend(mapped_objects)
          if mapped_columns:
               self._query = self._query_type(*mapped_columns)
          return self
               
     def count(self) -> Self:
          """Получение количества записей из таблицы

               Returns:
                    Self
          """
          self._query = self._query_type(func.count()).select_from(self._model)
          return self
               
     def join(self, relationship_strategy: list[str]) -> Self:
          """
               На вход приходит какая-то relationship_strategy.
               Далее происходит разбивка элемента списка по '.',
               затем устанавливается current_model. По мере того,
               как relationship будут уходить глубже current_model будет меняться.
               
               Пример 1: 
                    - на вход методу приходит ["skin"]
                    - сразу рассмотрю цикл 'for part in strategy part'
                    - current_model будет SkinWear
                    
                    Если у SkinWear будет атрибут skin, то случится следующее:
                    Достаём инстанс _RelationshipDeclared, далее current_model становится Skin,
                    т. к. Skin является orm объектом указанным в Mapped атрибута 'skin' класса SkinWear
                    
                    На выходе получаем множество: {SkinWear.skin}
                    Почему множество? - рассмотрено в следующем примере
                    
               Пример 2:
                    - на вход методу приходит ["skin", "skin.collections"]
                    - сразу рассмотрю цикл 'for part in strategy part'
                    - current_model будет SkinWear

                    Теперь начнём с "skin.collection", после метода split
                    получаем список из двух строк - ["skin", "collection"].
                    Сначала current_model это SkinWear, после получаем
                    _RelationshipDeclared(SkinWear.skin), и current_model изменяем
                    на Skin(объект, который указан в Mapped для отношения 'skin').
                    Теперь стоит прокрутить предыдущее предложение также, но уже
                    для 'collections'.
                    
                    Также уточню для чего нужен 'set(joined)'
                    По окончанию алгоритма в joined будет [SkinWear.skin, SkinWear.skin, Skin.collections]
                    создание множества помогает удалить нам повторяющаеся объекты.
          Args:
              relationship_strategy (list[str]): relationships, из которых складываются join-ы 
              
          Raises:
              ValueError: модель не имеет relationship поля из strategy part

          Returns:
              Self
          """
          joined = []
          for strategy in relationship_strategy:
               strategy_parts = strategy.split(".")
               
               current_model = self._model
               for part in strategy_parts:
                    if hasattr(current_model, part):
                         relationship: _RelationshipDeclared = getattr(current_model, part)
                         current_model: Base = relationship.mapper.class_
                         joined.append(relationship)
                    else:
                         raise ValueError(
                              f"JOIN: model {current_model} has not attribute {part} in strategy {strategy}"
                         )
          set_joined = set(joined)
          for join in set_joined:
               self._query = self._query.join(join)
          return self

     def where(self, data: dict[str, list[SQLAlchemyWhereCondition]]) -> Self:
          """Условия для запроса
          
               Итеруюсь по data, берём table_name, conditions
               Получаем orm объект таблицы и далле, вызываем метод __call__
               у класса SQLAlchemyCondition и получаем готовое условие
               
          Raises:
               ValueError: table not exists

          Args:
               data (dict[str, list[SQLAlchemyWhereCondition]])
                    Ключ - название таблицы
                    Значение - список условий для разных полей таблицы

          Returns:
              Self
          """
          where = []
          for table_name, conditions in data.items():
               orm_obj = self._orm_objects.get(table_name)
               if orm_obj is None:
                    raise ValueError(f"table {table_name} not exists")
               
               for cond in conditions:
                    value = cond(model=orm_obj)
                    if isinstance(value, list, tuple):
                         where.extend(value)
                    else:
                         where.append(value)
          self._query = self._query.where(*where)
          return self
          
     def order_by(self, data: dict[str, list[SQLAlchemyOrderByCondition]]) -> Self:
          """Сортировка по полю

          Args:
              data (dict[str, list[SQLAlchemyOrderByCondition]]): аналогично методу where

          Returns:
              Self: _description_
          """
          order_by = []
          for table_name, oby_condition in data.items():
               orm_obj = self._orm_objects.get(table_name)
               if orm_obj is None:
                    raise TypeError(f"table {table_name} not exists")
               
               for condition in oby_condition:
                    order_by_object = condition(model=self._model)
                    order_by.append(order_by_object)
          
          if order_by:
               self._query = self._query.order_by(*order_by)
          return self
     
     def values(self, data: dict[str, Any] | list[dict[str, Any]]) -> Self:
          """Метод используется для insert, update запросов
          
          Args:
              data (dict[str, Any] | list[dict[str, Any]], optional) данные для сохранения в бд
              
          Raises:
               TypeError: method values only for update or insert

          Returns:
              Self: _description_
          """
          if not isinstance(self._query, Insert, Update):
               raise TypeError("method values only for update, insert")
          
          if data:
               if isinstance(data, dict):
                    self._query = self._query.values(**data)
               else:
                    self._query = self._query.values(data)
          return self
   
     def limit(self, value: int | None = None) -> Self:
          if value:
               self._query = self._query.limit(value)
          return self
          
     def offset(self, value: int | None = None) -> Self:
          if value:
               self._query = self._query.offset(value)
          return self
   
     def returning(self, value: str | None = None) -> Self:
          """Значение поля, которое нужно вернуть, после выполнения запроса.
          
               Args:
                    value (str | None, optional): атрибут, существующее у модели
               
               Raises:
                    ValueError: 'RETURNING: model has no attribute value'
                    TypeError: method only for insert, update, delete

               Returns:
                    Self
          """
          if not isinstance(self._query, Insert, Update, Delete):
               raise TypeError("method only for insert, update, delete")
               
          if value:
               if hasattr(self._model, value):
                    self._query = self._query.returning(getattr(self._model, value))
               else:
                    raise ValueError(f"RETURNING: model {self._model} has no attribute {value}")
          return self
   
     def joinedload(self, relationship_strategy: list[str]) -> Self:
          """
               Здесь всё работает аналогично методу join, но отличия всё же есть.
               
               Добавляется ещё одна переменная current_joinedload.
               Сразу хочется уточнить, вот что:
                    Возьмём таблицы SkinWear и Skin.
                    Если мы захотим сделать select таблицы SkinWear и
                    в options добавить joinedload, то если мы захотим
                    для скина достать скин и коллекции, то синтаксис запроса 
                    будет таким: 
                    
                    select(SkinWear).
                    options(
                         joinedload(SkinWear.skin), 
                         joinedload(SkinWear.skin).joinedload(Skin.collections)
                    )
                    Теперь подведя к мысли, я могу сказать, что
                    current_joinedload он составляет цепочку из joinedload
          Args:
              relationship_strategy (list[str]): relationships, из которых складываются join-ы 
              
          Raises:
              ValueError: модель не имеет relationship поля из strategy part

          Returns:
              Self
          """
          joinedloads = []
          
          for strategy in relationship_strategy:
               strategy_parts = strategy.split(".")
               
               current_joinedload = None
               current_model = self._model
               for part in strategy_parts:
                    if hasattr(current_model, part):
                         relationship: _RelationshipDeclared = getattr(current_model, part)
                         current_model: Base = relationship.mapper.class_
                         if current_joinedload is None:
                              current_joinedload = joinedload(relationship)
                         else:
                              current_joinedload = current_joinedload.joinedload(relationship)
                    else:
                         raise ValueError(
                              f"JOINEDLOAD: model {current_model} has not attribute {part} in strategy {strategy}"
                         )
               joinedloads.append(current_joinedload)
          
          if joinedloads:
               self._query = self._query.options(*joinedloads)
          return self
     
     def build(self) -> Any:
          return self._query