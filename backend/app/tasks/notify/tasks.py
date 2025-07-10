import asyncio

from datetime import timedelta

from .base import BaseNotifyTask


class NotifyTask:
     def __init__(self):
          self.base_task = BaseNotifyTask()
     
     
     async def run(self) -> None:
          asyncio.create_task(self._day())
          asyncio.create_task(self._week())
          asyncio.create_task(self._month())
          
          
     async def _day(self) -> None:
          await asyncio.sleep(timedelta(days=1).total_seconds())
          await self.base_task.start(time=timedelta(days=1))
          await self._day()
          
          
     async def _week(self) -> None:
          await asyncio.sleep(timedelta(days=7).total_seconds())
          await self.base_task.start(time=timedelta(days=7))
          await self._week()
          
     
     async def _month(self) -> None:
          await asyncio.sleep(timedelta(days=30).total_seconds())
          await self.base_task.start(time=timedelta(days=30))
          await self._month()