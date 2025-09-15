import asyncio

from datetime import timedelta

from app.logger import logger

from .base import UpdatePriceAtDaysBase
from ..base import AbstarctTask




class UpdatePriceAtDaysTask(UpdatePriceAtDaysBase, AbstarctTask):
     
     async def run(self) -> None:
          logger.task_price_at_days.info("TASK UPDATE PRICE AT DAYS START")
          
          asyncio.create_task(self.run_price_at_days())
          
     async def run_price_at_days(self) -> None:
          logger.task_price_at_days.info("2 HOUR 30 MINUTES START")
          
          await asyncio.sleep(timedelta(hours=2, minutes=30).total_seconds())
          asyncio.create_task(self._process())
          await self.run_price_at_days()