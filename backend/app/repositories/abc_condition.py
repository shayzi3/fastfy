from typing import Protocol, Any

from app.schemas.enums import WhereConditionEnum, OrderByModeEnum




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
        
        
class BaseOrderByCondition(Protocol):
    
    def __init__(
        self,
        column: str,
        mode: OrderByModeEnum 
    ) -> None:
        self._column = column
        self._mode = mode
        
    def __call__(self, model: Any) -> Any:
        ...