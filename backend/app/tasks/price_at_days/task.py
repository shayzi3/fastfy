import asyncio

from datetime import timedelta

from .base import UpdatePriceAtDaysBase
from ..base import AbstarctTask




class UpdatePriceAtDaysTask(UpdatePriceAtDaysBase, AbstarctTask):
     
     async def run(self) -> None:
          asyncio.create_task(self.run_price_at_days())
          
     async def run_price_at_days(self) -> None:
          await asyncio.sleep(timedelta(hours=2, minutes=30).total_seconds())
          await self._process()
          await self.run_price_at_days()