
from typing import Any
from app.db.repository import SkinPriceHistoryRepository
from app.responses.abstract import AbstractResponse



class SkinPriceHistoryService:
     def __init__(self):
          self.repository = SkinPriceHistoryRepository
          
          
     async def history(
          self,
          skin_id: str | None = None,
          skin_name: str | None = None
     ) -> AbstractResponse | list[dict[str, Any]]:
          args = {
               "skin_id": skin_id
          } if skin_id is not None else {
               "skin_name": skin_name
          }
          result = await self.repository.filter_timestamp(**args)
          return result
          
          
          
async def get_price_history_service() -> SkinPriceHistoryService:
     return SkinPriceHistoryService()