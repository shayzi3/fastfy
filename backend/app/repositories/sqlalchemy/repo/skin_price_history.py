import json

from sqlalchemy import select

from datetime import timedelta, datetime

from app.schemas import SkinPriceHistoryModel
from backend.app.infrastracture.cache.abc import Cache
from app.schemas.dto import SkinPriceHistoryDTO
from app.db.models import SkinPriceHistory
from ..reposiotry import SQLAlchemyRepository


class SQLAlchemySkinPriceHisoryRepository(
     SQLAlchemyRepository[SkinPriceHistoryDTO, SkinPriceHistory]
):
     model = SkinPriceHistory
     
     
     async def price_by_timestamp(
          self, 
          timestamps: list[tuple[timedelta, str]],
          cache: Cache | None = None,
          cache_key: str | None = None,
          **where_kwargs
     ) -> dict[str, list[SkinPriceHistoryModel]]:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    loads_data: dict[str, list[str]] = json.loads(data)
                    return {
                         label: [SkinPriceHistoryModel.model_validate(json.loads(model)) for model in value]
                         for label, value in loads_data.items()
                    }
               
          query = (
               select(
                    self.model.price,
                    self.model.volume,
                    self.model.timestamp,
                    *[
                         (
                              self.model.timestamp >= datetime.now() - timestamp
                         ).label(label)
                         for timestamp, label in timestamps
                    ]
               ).
               filter_by(**where_kwargs).
               order_by(self.model.order_by())
          )
          result = await self.session.execute(query)
          result = result.all()
               
          if not result:
               return {}
               
          sort_by_labels = {label: [] for _, label in timestamps}
          for skin in result:
               price_history_obj = SkinPriceHistoryModel(
                    price=skin[0],
                    volume=skin[1],
                    timestamp=skin[2]
               )
               for index, label in enumerate(sort_by_labels.keys()):
                    if skin[3:][index] is True:
                         sort_by_labels[label].append(price_history_obj)
          
          if cache and cache_key:
               dump_models = {
                    label: [model.model_dump_json() for model in value] 
                    for label, value in sort_by_labels.items()
               }
               await cache.set(
                    name=cache_key,
                    value=json.dumps(dump_models),
                    ex=300
               )
          return sort_by_labels