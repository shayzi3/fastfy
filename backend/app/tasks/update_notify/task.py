import asyncio

from datetime import timedelta

from app.schemas.enums import UpdateMode

from .base import UpdateNotifyBase



class UpdateNotifyTask(UpdateNotifyBase):
     def __init__(self):
          super().__init__()
          
     
     async def run(self) -> None:
          asyncio.create_task(self.run_every_one_hour())
          asyncio.create_task(self.run_every_two_hour())
          asyncio.create_task(self.run_every_three_hour())
          asyncio.create_task(self.run_every_four_hour())
          
          
     async def run_every_one_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=1).total_seconds())
          await self._process(mode=UpdateMode.HIGH)
          await self.run_every_one_hour()
     
     
     async def run_every_two_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=2).total_seconds())
          await self._process(mode=UpdateMode.MEDIUM_WELL)
          await self.run_every_two_hour()
     
     
     async def run_every_three_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=3).total_seconds())
          await self._process(mode=UpdateMode.MEDIUM)
          await self.run_every_three_hour()
     
     
     async def run_every_four_hour(self) -> None:
          await asyncio.sleep(timedelta(hours=4).total_seconds())
          await self._process(mode=UpdateMode.LOW)
          await self.run_every_four_hour()