import asyncio

from app.schemas.enums import UpdateMode

from .base import BaseUpdatePricesTasks




class UpdatePricesTasks:
     def __init__(self):
          self.base_tasks = BaseUpdatePricesTasks()
     
     
     async def run(self) -> None:
          asyncio.create_task(self.one_hour())
          asyncio.create_task(self.two_hour())
          asyncio.create_task(self.three_hour())
          asyncio.create_task(self.four_hour())
          
          
     async def one_hour(self) -> None:
          await asyncio.sleep(1 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.HIGH)
          await self.one_hour()
          
          
     async def two_hour(self) -> None:
          await asyncio.sleep(2 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.MEDIUM_WELL)
          await self.two_hour()
          
     
     async def three_hour(self) -> None:
          await asyncio.sleep(3 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.MEDIUM)
          await self.three_hour()
          
          
     async def four_hour(self) -> None:
          await asyncio.sleep(4 * 3600)
          await self.base_tasks.update_all_skins(mode=UpdateMode.LOW)
          await self.four_hour()