import asyncio

from datetime import timedelta

from bot.logger import logger
from .base import BaseNotifyTask
from ..base import AbstractTask



class NotifyTask(BaseNotifyTask, AbstractTask):
     def __init__(self):
          super().__init__()
          
     
     async def run(self) -> None:
          logger.notify_task.info("RUN NOTIFY TASK")
          asyncio.create_task(self.run_every_five_minutes())
          
          
     async def run_every_five_minutes(self) -> None:
          logger.notify_task.info("RUN EVERY FIVE MINUTES START")
          
          await asyncio.sleep(timedelta(minutes=5).total_seconds())
          asyncio.create_task(self._process())
          await self.run_every_five_minutes()