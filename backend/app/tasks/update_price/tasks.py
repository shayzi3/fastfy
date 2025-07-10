import asyncio

from datetime import timedelta

from app.schemas.enums import UpdateMode

from .base import BaseUpdatePricesTasks




class UpdatePricesTasks:
     def __init__(self):
          self.base_task = BaseUpdatePricesTasks()
     
     
     async def run(self) -> None:
          asyncio.create_task(self._one_hour())
          asyncio.create_task(self._two_hour())
          asyncio.create_task(self._three_hour())
          asyncio.create_task(self._four_hour())
          
          
     async def _one_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=1).total_seconds())
          await self.base_task.start(mode=UpdateMode.HIGH)
          await self._one_hour()
          
          
     async def _two_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=2).total_seconds())
          await self.base_task.start(mode=UpdateMode.MEDIUM_WELL)
          await self._two_hour()
          
     
     async def _three_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=3).total_seconds())
          await self.base_task.start(mode=UpdateMode.MEDIUM)
          await self._three_hour()
          
          
     async def _four_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=4).total_seconds())
          await self.base_task.start(mode=UpdateMode.LOW)
          await self._four_hour()