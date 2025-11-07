from typing import Any

from app.schemas.enums import WhereConditionEnum
from app.repositories.abc_condition import BaseWhereCondition



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
        column_obj = getattr(model, self._column, None)
        if column_obj is not None:
            return self._all_conditions[self._cond.value](column_obj)