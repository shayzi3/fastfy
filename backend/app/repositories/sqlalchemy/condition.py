from typing import Any

from sqlalchemy import asc, desc

from app.schemas.enums import WhereConditionEnum, OrderByModeEnum
from app.repositories.abc_condition import BaseWhereCondition, BaseOrderByCondition



class SQLAlchemyWhereCondition(BaseWhereCondition):
    
    def __init__(
        self,
        column: str, 
        value: Any, 
        cond: WhereConditionEnum
    ) -> None:
        self._column = column
        self._value = value
        self._cond = cond
        
        self._all_conditions = {
            "=": lambda column_obj: column_obj == self._value,
            ">": lambda column_obj: column_obj > self._value,
            ">=": lambda column_obj: column_obj >= self._value,
            "<": lambda column_obj: column_obj < self._value,
            "<=": lambda column_obj: column_obj <= self._value,
            "ilike": lambda column_obj: [column_obj.ilike(f"%{part}%") for part in self._value.split()],
            "in": lambda column_obj: column_obj.in_(self._value)
        }
    
    def __call__(self, model: type) -> Any:
        if hasattr(model, self._column):
            mapped_object = getattr(model, self._column)
            return self._all_conditions[self._cond.value](mapped_object)
        else:
            raise TypeError(f"model {model} has no attribute {self._column}")
            
        
        
class SQLAlchemyOrderByCondition(BaseOrderByCondition):
    
    def __init__(
        self, 
        column: str, 
        mode: OrderByModeEnum
    ) -> None:
        self._column = column
        self._mode = mode
        
    def __call__(self, model: Any) -> Any:
        if hasattr(model, self._column):
            mapped_object = getattr(model, self._column)
            mode = asc if self._mode == OrderByModeEnum.ASC else desc
            return mode(mapped_object)
        else:
            raise TypeError