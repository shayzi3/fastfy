from typing import Any
from datetime import timedelta

from app.schemas.enums import OrderByModeEnum
from app.repositories.abc_condition import BaseWhereCondition
from app.infrastracture.cache.abc import Cache
from app.schemas.dto import SkinPriceHistoryDTO
from app.schemas import SkinPriceHistoryModel
from ..abc_repository import BaseRepository


class BaseSkinPriceHistoryRepository(BaseRepository[SkinPriceHistoryDTO, Any]):
     
     async def price_by_timestamp(
          self, 
          timestamps: list[tuple[timedelta, str]],
          where: dict[str, list[BaseWhereCondition]] = {},
          order_by: dict[str, list[tuple[str, OrderByModeEnum]]] = {},
          cache: Cache | None = None,
          cache_key: str | None = None,
     ) -> dict[str, list[SkinPriceHistoryModel]]:
          ...