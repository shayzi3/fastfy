import json

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
     SkinPriceHistoryModel, 
     SkinHistoryModel, 
     SkinHistoryTimePartModel
)
from app.db.models import SkinsPriceHistory
from app.infrastracture.redis import RedisPool
from .base import BaseRepository



class SkinPriceHistoryRepository(
     BaseRepository[SkinPriceHistoryModel, None]
):
     model = SkinsPriceHistory
                    
          
     @classmethod
     async def filter_timestamp(
          cls, 
          session: AsyncSession,
          redis_session: RedisPool,
          redis_key: str,
          **where_args
     ) -> SkinHistoryTimePartModel:
          redis_result = await redis_session.hgetall(redis_key)
          
          if not redis_result:
               sttm = (
                    select(
                         cls.model.price,
                         cls.model.volume,
                         cls.model.timestamp,
                         (cls.model.timestamp <= datetime.now()).label("all"),
                         (cls.model.timestamp >= datetime.now() - timedelta(days=365)).label("year"),
                         (cls.model.timestamp >= datetime.now() - timedelta(days=30)).label("month"),
                         (cls.model.timestamp >= datetime.now() - timedelta(days=1)).label("day"),
                    ).
                    filter_by(**where_args).
                    order_by(cls.model.timestamp)
               )
               result = await session.execute(sttm)
               result = result.all()
               
               returning = await cls.__item_sorted(items=result)
               await cls.__redis_pipeline(
                    session=redis_session,
                    data=returning,
                    redis_key=redis_key
               )
               return SkinHistoryTimePartModel(**returning)
          
          return SkinHistoryTimePartModel(
               all=json.loads(redis_result["all"]),
               year=json.loads(redis_result["year"]),
               month=json.loads(redis_result["month"]),
               day=json.loads(redis_result["day"]),
          )
          
          
     @staticmethod
     async def __redis_pipeline(
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
     async def __item_sorted(
          items: Any
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
          
               