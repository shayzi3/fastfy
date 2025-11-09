import json

from sqlalchemy import select

from datetime import timedelta, datetime

from app.schemas.enums import WhereConditionEnum, OrderByModeEnum
from app.schemas import SkinPriceHistoryModel
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_condition import BaseWhereCondition
from app.schemas.dto import SkinPriceHistoryDTO
from app.db.models import SkinPriceHistory
from ..repository import SQLAlchemyRepository


class SQLAlchemySkinPriceHisoryRepository(
     SQLAlchemyRepository[SkinPriceHistoryDTO, SkinPriceHistory]
):
     model = SkinPriceHistory
     
     
     async def price_by_timestamp(
          self, 
          timestamps: list[tuple[timedelta, str]],
          where: dict[str, list[BaseWhereCondition]] = {},
          order_by: dict[str, list[tuple[str, OrderByModeEnum]]] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
          **kwargs
     ) -> dict[str, list[SkinPriceHistoryModel]]:
          if cache and cache_key:
               data = await cache.get(name=cache_key)
               if data:
                    loads_data: dict[str, list[str]] = json.loads(data)
                    return {
                         label: [SkinPriceHistoryModel.model_validate(json.loads(model)) for model in value]
                         for label, value in loads_data.items()
                    }
               
          query = await self._query_builder(
               type_=select,
               columns=[
                    "price", "volume", "timestamp",
                    *[(self.model.timestamp >= datetime.now() - timestamp).label(label) 
                      for timestamp, label in timestamps
                    ]
               ],
               where=where,
               order_by=order_by
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