from typing import Any
from datetime import timedelta

from app.infrastracture.cache.abc import Cache
from app.schemas.dto import SkinPriceHistoryDTO
from app.schemas import SkinPriceHistoryModel
from ..abc_repository import BaseRepository


class BaseSkinPriceHistoryRepository(BaseRepository[SkinPriceHistoryDTO, Any]):
     
     async def price_by_timestamp(
          self,
          timestamps: list[tuple[timedelta, str]],
          cache: Cache | None = None,
          cache_key: str | None = None,
          **where_kwargs
     ) -> dict[str, list[SkinPriceHistoryModel]]:
          ...