from app.schemas import SkinPriceHistoryModel
from app.db.models import SkinsPriceHistory

from .base import BaseRepository


class SkinPriceHistoryRepository(
     BaseRepository[SkinPriceHistoryModel, None]
):
     model = SkinsPriceHistory
     
     
     @classmethod
     async def read_all(cls) -> list[SkinPriceHistoryModel]:
          ...
          
          
     @classmethod
     async def filter_timestamp(cls) -> list[SkinPriceHistoryModel]:
          ...