import asyncio

from app.schemas.enums import UpdateMode

from .base import BaseUpdatePricesTasks




class UpdatePricesTasks:
     def __init__(self):
          self.base_tasks = BaseUpdatePricesTasks()
     
     
     async def run(self) -> None:
          asyncio.create_task(self._one_hour())
          asyncio.create_task(self._two_hour())
          asyncio.create_task(self._three_hour())
          asyncio.create_task(self._four_hour())
          
          
     async def _one_hour(self) -> None:
          await asyncio.sleep(1 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.HIGH)
          await self._one_hour()
          
          
     async def _two_hour(self) -> None:
          await asyncio.sleep(2 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.MEDIUM_WELL)
          await self._two_hour()
          
     
     async def _three_hour(self) -> None:
          await asyncio.sleep(3 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.MEDIUM)
          await self._three_hour()
          
          
     async def _four_hour(self) -> None:
          await asyncio.sleep(4 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.LOW)
          await self._four_hour()