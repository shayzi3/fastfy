import asyncio

from .base import BaseNotifyTask


class NotifyTask:
     def __init__(self):
          self.base_notify_task = BaseNotifyTask()
     
     
     async def run(self) -> None:
          asyncio.create_task(self._notify_day())
          asyncio.create_task(self._notify_week())
          asyncio.create_task(self._notify_month())
          
          
     async def _notify_day(self) -> None:
          await asyncio.sleep(1 * 86400)
          await self.base_notify_task.explore_skins(mode="day")
          await self._notify_day()
          
          
     async def _notify_week(self) -> None:
          await asyncio.sleep(7 * 86400)
          await self.base_notify_task.explore_skins(mode="week")
          await self._notify_week()
          
     
     async def _notify_month(self) -> None:
          await asyncio.sleep(30 * 86400)
          await self.base_notify_task.explore_skins(mode="month")
          await self._notify_month()