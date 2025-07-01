import aiohttp
import asyncio
import loguru
import random

from string import digits

from datetime import datetime
from dataclasses import dataclass

from app.db.repository import SkinRepository, SkinPriceHistoryRepository


@dataclass
class CaseItem:
     id: str
     name: str
     image: str   
     
     
def generate_id():
     return int("".join([str(random.choice(digits)) for _ in range(10)]))


class CaseStill:
     def __init__(self):
          self.url = (
               "https://steamfolio.com/api/Popular/" +
               "sort?type=3&ascending=false&watchlist=false&searchTerm=&filterType=2&page="
          )
          
          
     async def still(self) -> None:
          for page in range(2, 101):
               loguru.logger.info(f"Page {page}")
               url = self.url + str(page)
               
               async with aiohttp.ClientSession() as session:
                    response = await session.get(url)
                    json_data = await response.json()
                    
               timer = 0
               gather_funcs = []
               items = json_data["data"]["items"]
               if not items:
                    return loguru.logger.info("Search items ending")
                    
               for skin in items:
                    item = CaseItem(
                         id=skin.get("id"),
                         name=skin.get("marketHashName"),
                         image=skin.get("image")
                    )
                    gather_funcs.append(self.item(item, timer))
                    timer += 2
               await asyncio.gather(*gather_funcs)
          
          
     async def item(self, skin: CaseItem, timer: int) -> None:
          skin_model = {
               "id": skin.id,
               "name": skin.name,
               "avatar": skin.image,
               "price": 0,
          }
          await asyncio.sleep(timer)
          async with aiohttp.ClientSession() as session:
               # price
               try:
                    response = await session.get(
                         (
                         "https://steamcommunity.com" + 
                         f"/market/priceoverview/?currency=1&appid=730&market_hash_name={skin.name.replace('&', '%26')}"
                         )
                    )
                    json_data = await response.json()
                    
                    price = json_data.get("lowest_price")
                    if price is None:
                         price = json_data.get("median_price")
                    skin_model["price"] = round(float(price[1:]), 2)
               except Exception as ex:
                    loguru.logger.error(ex)
                    await self.item(skin, timer + 5)
               
               # price history
               response = await session.get(
                    url=f"https://steamfolio.com/api/Graph/itemChart?name={skin.name.replace('&', '%26')}"
               )
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
                              "item_id": generate_id(),
                              "skin_id": skin.id,
                              "skin_name": skin.name,
                              "price": round(float(part["value"]), 2),
                              "volume": volume[index]["value"],
                              "timestamp": time
                         }
                    )
                    
               item_exists = await SkinRepository.read(id=skin.id)
               if item_exists is None:
                    try:
                         await SkinRepository.create(data=skin_model)
                         await SkinPriceHistoryRepository.create(data=price_history)
                    except Exception as ex:
                         print(ex)
                    return loguru.logger.info(f"Skin {skin.name} in db")
               loguru.logger.info(f"Item {skin.name} already exists")
               
               
          
          
async def main_still():
     cases = CaseStill()
     await cases.still()
     
     