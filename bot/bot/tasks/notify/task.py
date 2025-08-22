import asyncio

from datetime import timedelta

from .base import BaseNotifyTask
from ..base import AbstractTask



class NotifyTask(BaseNotifyTask, AbstractTask):
     def __init__(self):
          super().__init__()
          
     
     async def run(self) -> None:
          asyncio.create_task(self.run_every_five_minutes())
          
          
     async def run_every_five_minutes(self) -> None:
          await asyncio.sleep(timedelta(minutes=5).total_seconds())
          asyncio.create_task(self._process())
          await self.run_every_five_minutes()