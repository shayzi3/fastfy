import asyncio

from datetime import timedelta

from app.schemas import SkinPriceInfoModel
from app.db.session import session_asynccontext
from app.db.repository import (
     SkinPriceInfoRepository, 
     SkinPriceHistoryRepository
)



class UpdatePriceAtDaysBase:
     
     
     async def _process(self) -> None:
          async with session_asynccontext() as async_session:
               skins = await SkinPriceInfoRepository.read_all(
                    session=async_session
               )
               if skins:
                    await asyncio.gather(
                         *[
                              self._skin_process(skin)
                              for skin in skins
                         ]
                    )
          
          
     async def _skin_process(
          self,
          skin: SkinPriceInfoModel
     ) -> None:
          async with session_asynccontext() as async_session:
               skin_price_history = await SkinPriceHistoryRepository.filter_timestamp(
                    session=async_session,
                    timestamps=[
                         (timedelta(days=365), "year"),
                         (timedelta(days=30), "month"),
                         (timedelta(days=1), "day")
                    ],
                    skin_name=skin.skin_name
               )
               update_data_at_skin = {}
               
               year, month, day = (
                    skin_price_history.get("year"),
                    skin_price_history.get("month"),
                    skin_price_history.get("day")
               )
               
               if year and len(year) >= 2:
                    update_data_at_skin.update(
                         {
                              "price_last_365_day": ((year[-1].price - year[0].price) / year[0].price) * 100
                         }
                    )
               if month and len(month) >= 2:
                    update_data_at_skin.update(
                         {
                              "price_last_30_day": ((month[-1].price - month[0].price) / month[0].price) * 100
                         }
                    )
               if day and len(day) >= 2:
                    update_data_at_skin.update(
                         {
                              "price_last_1_day": ((day[-1].price - day[0].price) / day[0].price) * 100
                         }
                    )
                    
               if update_data_at_skin:
                    await SkinPriceInfoRepository.update(
                         session=async_session,
                         where={"skin_name": skin.skin_name},
                         **update_data_at_skin
                    )
                    
               