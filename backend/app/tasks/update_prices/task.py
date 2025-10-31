import asyncio

from datetime import timedelta

from app.schemas.enums import UpdateMode
from backend.app.utils.logger import logger

from .base import UpdateNotifyBase
from ..base import AbstarctTask



class UpdateNotifyTask(UpdateNotifyBase, AbstarctTask):
     def __init__(self):
          super().__init__()
          
     
     async def run(self) -> None:
          logger.task_update_notify.info("TASK UPDATE NOTIFY START")
          
          asyncio.create_task(self.run_every_one_hour())
          asyncio.create_task(self.run_every_two_hour())
          asyncio.create_task(self.run_every_three_hour())
          asyncio.create_task(self.run_every_four_hour())
          
          
     async def run_every_one_hour(self) -> None:
          logger.task_update_notify.info("1 HOUR START")
          
          await asyncio.sleep(timedelta(hours=1).total_seconds())
          asyncio.create_task(self._process(mode=UpdateMode.HIGH))
          await self.run_every_one_hour()
     
     
     async def run_every_two_hour(self) -> None:
          logger.task_update_notify.info("2 HOUR START")
          
          await asyncio.sleep(timedelta(hours=2).total_seconds())
          asyncio.create_task(self._process(mode=UpdateMode.MEDIUM_WELL))
          await self.run_every_two_hour()
     
     
     async def run_every_three_hour(self) -> None:
          logger.task_update_notify.info("3 HOUR START")
          
          await asyncio.sleep(timedelta(hours=3).total_seconds())
          asyncio.create_task(self._process(mode=UpdateMode.MEDIUM))
          await self.run_every_three_hour()
     
     
     async def run_every_four_hour(self) -> None:
          logger.task_update_notify.info("4 HOUR START")
          
          await asyncio.sleep(timedelta(hours=4).total_seconds())
          asyncio.create_task(self._process(mode=UpdateMode.LOW))
          await self.run_every_four_hour()