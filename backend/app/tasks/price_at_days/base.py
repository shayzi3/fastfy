import asyncio

from datetime import timedelta

from app.db.repository import SkinRepository, SkinPriceHistoryRepository
from app.db.session import Session
from app.infrastracture.redis import RedisPool
from app.schemas.enums import UpdateMode
from app.schemas import SkinModel



class BasePriceAtDaysTask:
     def __init__(self):
          self.skin_repository = SkinRepository
          self.history_repository = SkinPriceHistoryRepository
          
          
     async def start(self, mode: UpdateMode) -> None:
          skins = await self.skin_repository.read_all_task_update_price(mode=mode)
          gather_funcs = []
          for skin in skins:
               gather_funcs.append(self._get_prices_at_skins(skin))
          await asyncio.gather(*gather_funcs)
          
          
     async def _get_prices_at_skins(self, skin: SkinModel) -> None:
          history = await self.history_repository.filter_timestamp_task_price_at_days(
               skin_name=skin.name
          )
          update_values = {
               "price_last_365_day": None,
               "price_last_30_day": None,
               "price_last_1_day": None
          }
          year = history.get("year")
          if year and len(year) >= 2:
               year_percent = round(((year[-1] - year[0]) / year[0]) * 100, 2)
               update_values["price_last_365_day"] = year_percent
               
          month = history.get("month")
          if month and len(month) >= 2:
               month_percent = round(((month[-1] - month[0]) / month[0]) * 100, 2)
               update_values["price_last_30_day"] = month_percent
               
               
          day = history.get("day")
          if day and len(day) >= 2:
               day_percent = round(((day[-1] - day[0]) / day[0]) * 100, 2)
               update_values["price_last_1_day"] = day_percent
          await self._update_prices_at_skins(skin, update_values)
               
               
     async def _update_prices_at_skins(
          self,
          skin: SkinModel,
          update_values: dict[str, float]
     ) -> None:
          async with Session.session() as async_session:
               pool = RedisPool()
               await self.skin_repository.update(
                    session=async_session,
                    where={"name": skin.name},
                    redis_session=pool,
                    delete_redis_values=[f"skin:{skin.name}"],
                    **update_values
               )
               await pool.close()
          