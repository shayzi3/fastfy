from typing import Protocol, Any

from app.schemas.enums import WhereConditionEnum




class BaseWhereCondition(Protocol):
    
    def __init__(
        self,
        column: str, 
        value: Any, 
        cond: WhereConditionEnum
    ) -> None:
        self._column = column
        self._value = value
        self._cond = cond
        
    def __call__(self, model: Any) -> Any:
        ...