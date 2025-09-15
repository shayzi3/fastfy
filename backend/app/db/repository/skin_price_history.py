import json

from datetime import datetime, timedelta
from typing import Any
from sqlalchemy import select

from app.db.session import AsyncSession
from app.schemas import (
     SkinPriceHistoryModel, 
     SkinHistoryModel
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
          timestamps: list[tuple[timedelta, str]],
          redis_session: RedisPool | None = None,
          redis_key: str | None = None,
          **where_args
     ) -> dict[str, list[SkinHistoryModel]]:
          if (redis_session is not None) and (redis_key is not None):
               redis_result = await redis_session.get(redis_key)
               if redis_result:
                    data = json.loads(redis_result)
                    return {
                         key: [SkinHistoryModel.model_validate(json.loads(obj)) for obj in value]
                         for key, value in data.items()
                    }
               
          sttm = (
               select(
                    SkinsPriceHistory.price,
                    SkinsPriceHistory.volume,
                    SkinsPriceHistory.timestamp,
                    *[
                         (
                              SkinsPriceHistory.timestamp >= datetime.now() - timestmp
                         ).label(label)
                         for timestmp, label in timestamps
                    ]
               ).
               filter_by(**where_args).
               order_by(SkinsPriceHistory.timestamp)
          )
          result = await session.execute(sttm)
          result = result.all()
               
          if not result:
               return {}
               
          sort_by_labels = {label: [] for _, label in timestamps}
          for skin in result:
               price_history_obj = SkinHistoryModel(
                    price=skin[0],
                    volume=skin[1],
                    timestamp=skin[2]
               )
               for index, label in enumerate(sort_by_labels.keys()):
                    if skin[3:][index] is True:
                         sort_by_labels[label].append(price_history_obj)
               
          if (redis_session is not None) and (redis_key is not None):
               dumping_to_json = {
                    key: [model.model_dump_json() for model in value]
                    for key, value in sort_by_labels.items()
               }
               await redis_session.set(
                    name=redis_key,
                    value=json.dumps(dumping_to_json),
                    ex=120
               )
          return sort_by_labels