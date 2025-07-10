import json

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select

from app.db.session import Session, AsyncSession
from app.schemas import (
     SkinPriceHistoryModel, 
     SkinHistoryTimePartModel
)
from app.db.models import SkinsPriceHistory
from app.infrastracture.redis import RedisPool
from app.db.utils import RepositoryUtils
from .base import BaseRepository

     




class SkinPriceHistoryRepository(
     BaseRepository[SkinPriceHistoryModel, None]
):
     model = SkinsPriceHistory
     _utils = RepositoryUtils
        
          
     @classmethod
     async def filter_timestamp(
          cls, 
          session: AsyncSession,
          redis_session: RedisPool,
          redis_key: str,
          **where_args
     ) -> SkinHistoryTimePartModel | None:
          redis_result = await redis_session.hgetall(redis_key)
          
          if not redis_result:
               sttm = (
                    select(
                         SkinsPriceHistory.price,
                         SkinsPriceHistory.volume,
                         SkinsPriceHistory.timestamp,
                         (SkinsPriceHistory.timestamp <= datetime.now()).label("all"),
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=365)).label("year"),
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=30)).label("month"),
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=1)).label("day"),
                    ).
                    filter_by(**where_args).
                    order_by(SkinsPriceHistory.timestamp)
               )
               result = await session.execute(sttm)
               result = result.all()
               
               if not result:
                    return None
               
               returning = await cls._utils.item_sorted(items=result)
               await cls._utils.redis_pipeline(
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
          
          
     @classmethod
     async def filter_timestamp_task_notify(
          cls,
          skin_name: str,
          time: timedelta
     ) -> list[dict[str, Any]]:
          async with Session.session() as async_session:
               sttm = (
                    select(
                         SkinsPriceHistory.price,
                         SkinsPriceHistory.timestamp,
                         (SkinsPriceHistory.timestamp >= datetime.now() - time).lanel("zone")
                    ).
                    where(SkinsPriceHistory.skin_name == skin_name).
                    order_by(SkinsPriceHistory.timestamp)
               )
               result = await async_session.execute(sttm)
               result = result.all()
          return await cls._utils.item_sorted_task_notify(result)
     
     
     @classmethod
     async def filter_timestamp_task_price_at_days(
          cls,
          skin_name: str
     ) -> list[dict[str, Any]]:
          async with Session.session() as async_session:
               sttm = (
                    select(
                         SkinsPriceHistory.price,
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=365)).label("year"),
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=30)).label("month"),
                         (SkinsPriceHistory.timestamp >= datetime.now() - timedelta(days=1)).label("day")
                    ).
                    where(SkinsPriceHistory.skin_name == skin_name).
                    order_by(SkinsPriceHistory.timestamp)
               )
               result = await async_session.execute(sttm)
               result = result.all()
          return await cls._utils.item_sorted_task_price_at_days(result)