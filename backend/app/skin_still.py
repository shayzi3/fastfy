import uuid
import aiohttp
import asyncio
import loguru
import random

from string import digits

from dataclasses import dataclass
from datetime import datetime

from app.db.session import Session
from app.db.repository import SkinRepository, SkinPriceHistoryRepository
from app.schemas.enums import UpdateMode


@dataclass
class CaseItem:
     name: str
     avatar: str   
     price: float
     update_mode: UpdateMode = UpdateMode.LOW
     
     
def generate_id():
     return int("".join([str(random.choice(digits)) for _ in range(10)]))


class CaseStill:
     def __init__(self):
          self.url = (
               "https://steamfolio.com/api/Popular/sort?type=2&ascending=false&watchlist=false&searchTerm=&filterType=4&page="
          )
          
          
     async def still(self) -> None:
          pages_funcs = []
          for page in range(1, 3):
               loguru.logger.info(f"Page {page}")
               url = self.url + str(page)
               
               async with aiohttp.ClientSession() as session:
                    async with await session.get(url) as response:
                         json_data = await response.json()
                         pages_funcs.append(self.pages(json_data, page))
          await asyncio.gather(*pages_funcs)
          
               
     async def pages(self, data, page):
          items = data["data"]["items"]
          if not items:
               return loguru.logger.info(f"Search items ending on page {page}")
                    
          async with Session.session() as async_session:
               for skin in items:
                    try:
                         item = CaseItem(
                              name=skin.get("marketHashName"),
                              avatar=skin.get("image"),
                              price=round(skin.get("safePrice"), 2)
                         )
                    except:
                         continue
                    await self.item(item, async_session)
          
          
     async def item(self, skin: CaseItem, async_session) -> None:
          async with aiohttp.ClientSession() as session:
               async with session.get(
                    url=f"https://steamfolio.com/api/Graph/itemChart?name={skin.name.replace('&', '%26')}"
               ) as response:
                    json_data = await response.json()
               
          price_history = []
          volume = json_data["data"]["all"]["volumes"]
          for index, part in enumerate(json_data["data"]["all"]["values"]):
               time = part["time"]
               if isinstance(time, int):
                    time = datetime.fromtimestamp(time)
                         
               elif isinstance(time, str):
                    time = datetime.fromisoformat(time)
                    
               price_history.append(
                    {
                         "item_id": uuid.uuid4(),
                         "skin_name": skin.name,
                         "price": round(float(part["value"]), 2),
                         "volume": volume[index]["value"],
                         "timestamp": time
                    }
               )
          
          last_volume = price_history[-2]["volume"]
          if last_volume >= 20000:
               skin.update_mode = UpdateMode.HIGH
               
          elif last_volume >= 8000:
               skin.update_mode = UpdateMode.MEDIUM_WELL
               
          elif last_volume >= 2000:
               skin.update_mode = UpdateMode.MEDIUM
          
          item_exists = await SkinRepository.read(name=skin.name, session=async_session)
          if item_exists is None:
               try:
                    await SkinRepository.create(data=skin.__dict__, session=async_session)
                    await SkinPriceHistoryRepository.create(data=price_history, session=async_session)
                    await async_session.close()
                    return loguru.logger.info(f"Skin {skin.name} in db")

               except Exception as ex:
                    print(ex, skin.name)
                    await async_session.close()
                    # await self.item(skin, timer + 1)
                    return 
          await async_session.close()                           
          loguru.logger.info(f"Item {skin.name} already exists")
               
               
          
          
async def main_still():
     cases = CaseStill()
     await cases.still()
     
     