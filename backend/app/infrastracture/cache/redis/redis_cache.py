from typing import Any
from redis.asyncio import Redis

from app.core import my_config
from ..abc import Cache





class CacheRedis(Cache):
     def __init__(self):
          self._connection = None
          
     async def __aenter__(self) -> None: 
          if not self._connection:
               self._connection = Redis(
                    host=my_config.redis_host,
                    port=my_config.redis_port,
                    password=my_config.redis_password,
                    decode_responses=True
               )
     
     async def __aexit__(self, *args) -> None:
          await self.close()
          self._connection = None
                  
     async def set(self, key: str, value: str, ex: int = 0) -> None:
          if self._connection:
               await self._connection.set(name=key, value=value, ex=ex)
          
     async def get(self, key: str) -> Any:
          if self._connection:
               return await self._connection.get(name=key)
          
     async def delete(self, *keys: str) -> None:
          if self._connection:
               await self._connection.delete(*keys)
               
     async def close(self) -> None:
          if self._connection:
               await self._connection.aclose()
               self._connection = None
          