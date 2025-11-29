import json

from typing_extensions import Self, Any
from dataclasses import dataclass
from datetime import timedelta, datetime

from fastapi import Request
from dishka.integrations.fastapi import inject, FromDishka

from app.infrastracture.cache.abc import Cache
from app.schemas import JWTTokenPayloadModel
from app.responses import TooManyRequestError


@dataclass
class RateLimitCacheData:
     exp: float
     current_try: int
     max_try: int
     
     def is_many_request(self) -> bool:
          return (self.current_try >= self.max_try) and (datetime.now() <= self.from_timestamp())
     
     def from_timestamp(self) -> datetime:
          return datetime.fromtimestamp(self.exp)
     
     @property
     def dump(self) -> dict[str, Any]:
          return self.__dict__

     def dump_json(self) -> str:
          return json.dumps(self.dump)
     
     @classmethod
     def from_json(cls, data: str) -> Self:
          return cls(**json.loads(data))



class RateLimitDepend:
     def __init__(self, reqs: int, at_time: timedelta, category: str):
          self._reqs = reqs
          self._at_time = at_time
          self._category = category
          
     def build_cache_key(self, keys: list[str] = []) -> str:
          return f":".join(["rate_limit", self._category, *keys])
          
     @inject
     async def __call__(self, cache: FromDishka[Cache], token_payload: FromDishka[JWTTokenPayloadModel]) -> None:
          async with cache:
               cache_data = await cache.get(self.build_cache_key(keys=[str(token_payload.uuid)]))
               if cache_data:
                    rate_limit_cache = RateLimitCacheData.from_json(cache_data)
                    if datetime.now() >= rate_limit_cache.from_timestamp():
                         rate_limit_cache.current_try = 0
                         rate_limit_cache.exp = (datetime.now() + self._at_time).timestamp()
                         
                    elif rate_limit_cache.is_many_request():
                         raise TooManyRequestError.exec()
                    
                    rate_limit_cache.current_try += 1
               else:
                    now = datetime.now()
                    rate_limit_cache = RateLimitCacheData(
                         exp=(now + self._at_time).timestamp(),
                         current_try=1,
                         max_try=self._reqs
                    )
               await cache.set(
                    key=self.build_cache_key(keys=[str(token_payload.uuid)]),
                    value=rate_limit_cache.dump_json(),
               )
          
           
          
          
          