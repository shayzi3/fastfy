from datetime import datetime, timedelta
from typing import Any

from app.schemas import SkinPriceHistoryModel
from app.db.models import SkinsPriceHistory

from sqlalchemy import select

from ..session import Session
from .base import BaseRepository


class SkinPriceHistoryRepository(
     BaseRepository[SkinPriceHistoryModel, None]
):
     model = SkinsPriceHistory
                    
          
     @classmethod
     async def filter_timestamp(
          cls, 
          **where_args
     ) -> list[dict[str, Any]]:
          async with Session.session() as async_session:
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
               result = await async_session.execute(sttm)
          
          returning = {"all": [], "year": [], "month": [], "day": []}
          data = result.all()
          for item in data:
               part = {
                    "price": item.price,
                    "volume": item.volume,
                    "timestamp": item.timestamp
               }
               if item.all:
                    returning["all"].append(part)
               if item.year:
                    returning["year"].append(part)
               if item.month:
                    returning["month"].append(part)
               if item.day:
                    returning["day"].append(part)
          return returning
          
               