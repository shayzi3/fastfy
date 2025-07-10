import json

from typing import Any

from app.infrastracture.redis import RedisPool
from app.schemas import SkinHistoryModel



class RepositoryUtils:
     
     
     @staticmethod
     async def redis_pipeline(
          session: RedisPool, 
          data: dict[str, Any],
          redis_key: str
     ) -> None:
          async with session.pipeline() as pipe:
               await pipe.hset(
                    name=redis_key,
                    mapping={
                         "all": json.dumps(data["all"]),
                         "year": json.dumps(data["year"]),
                         "month": json.dumps(data["month"]),
                         "day": json.dumps(data["day"])
                    }
               )
               await pipe.expire(
                    name=redis_key,
                    time=1000
               )
               await pipe.execute()
               
               
     @staticmethod
     async def item_sorted(
          items: list[Any]
     ) -> dict[str, list[dict[str, Any]]]:
          returning = {"all": [], "year": [], "month": [], "day": []}
          for item in items:
               part = SkinHistoryModel(
                    price=item.price,
                    volume=item.volume,
                    timestamp=item.timestamp.isoformat()
               ).model_dump()
                    
               if item.all:
                    returning["all"].append(part)
               if item.year:
                    returning["year"].append(part)
               if item.month:
                    returning["month"].append(part)
               if item.day:
                    returning["day"].append(part)
          return returning
     
     
     @staticmethod
     async def item_sorted_task_notify(
          items: list[Any]
     ) -> list[dict[str, Any]]:
          returning = []
          for item in items:
               if item.zone:
                    returning.append(
                         {
                              "price": item.price, 
                              "timestamp": item.timestamp.isoformat()
                         }
                    )
          return returning
     
     
     @staticmethod
     async def item_sorted_task_price_at_days(
          items: list[Any]
     ) -> list[dict[str, list[int]]]:
          returning = {"year": [], "month": [], "day": []}
          for item in items:
               if item.year:
                    returning["year"].append(item.price)
               if item.month:
                    returning["month"].append(item.price)
               if item.day:
                    returning["day"].append(item.price)
          return returning