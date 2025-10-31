from typing import Protocol, Any
from typing_extensions import Self




class Cache(Protocol):
     
     def __init__(self):
          self._connection = None
     
     async def __aenter__(self) -> Any:
          ...
          
     async def __aexit__(self) -> None:
          ...
      
     async def set(self, key: str, value: Any, ex: int = 0) -> Any:
          ...
     
     async def get(self, key: str) -> Any:
          ...
          
     async def delete(self, *keys: str) -> None:
          ...
          
     async def close(self) -> None:
          ...