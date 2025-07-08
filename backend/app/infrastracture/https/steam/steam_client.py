import uuid
import aiohttp
import json

from datetime import datetime
from typing import Any

from app.core import my_config
from app.infrastracture.redis import RedisPool
from app.responses.abstract import AbstractResponse
from app.responses import HttpError, SkinNotFoundError
from app.schemas import SteamItem, SkinModel




class HttpSteamClient:
     def __init__(self):
          self.api_key = my_config.steam_api_key
          self.icon_url = "https://community.akamai.steamstatic.com/economy/image/"
     
     
     async def get_steam_profile(self, steamids: int) -> tuple[str, str] | AbstractResponse:
          url = (
               "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/" +
               f"?key={self.api_key}&steamids={steamids}"
          )
          async with aiohttp.ClientSession() as session:
               for _ in range(3):
                    try:
                         async with session.get(url) as response:
                              data = await response.json()
                              break
                    except:
                         continue
               else:
                    return HttpError
               
               response = data.get("response")
               if "players" in response and response.get("players"):
                    players = response.get("players")[0]
                    return (players.get("personaname"), players.get("avatarmedium"))
               return HttpError
               
               
     async def get_steam_inventory(self, steamid: int) -> list[SteamItem] | AbstractResponse:
          url = f"https://steamcommunity.com/inventory/{steamid}/730/2"
          
          async with aiohttp.ClientSession() as session:
               for _ in range(3):
                    try:
                         async with session.get(url) as response:
                              # errors
                              data = await response.json()
                              break
                    except:
                         continue
               else:
                    return HttpError
               
               assets = data.get("assets")
               descriptions = data.get("descriptions")
               
               quantity_skins = {}
               for item in assets:
                    if item.get("classid") not in quantity_skins.keys():
                         quantity_skins[item.get("classid")] = 0
                    quantity_skins[item.get("classid")] += 1
                    
               inventory = []
               for inventory_item in descriptions:
                    if inventory_item.get("marketable") == 1:
                         inventory.append(
                              SteamItem(
                                   name=inventory_item.get("market_hash_name"),
                                   avatar=self.icon_url + inventory_item.get("icon_url"),
                                   quantity=quantity_skins.get(inventory_item.get("classid")),
                              )
                         )
               return inventory
               
               
     async def search_steam_skins(
          self,
          redis_session: RedisPool,
          query: str,
          offset: int,
     ) -> list[dict[str, Any]] | AbstractResponse:
          key = f"search:{query}:offset={offset}"
          skins = await redis_session.get(key)
          if skins is not None:
               skins = json.loads(skins)
          
          url = (
               "https://steamcommunity.com/market/search/render/"
               f"?query={query}&start={offset}&count=10&search_descriptions=0"
               "&sort_column=default&sort_dir=desc&appid=730&norender=1"
          )
          if skins is None:
               async with aiohttp.ClientSession() as session:
                    for _ in range(3):
                         try:
                              async with session.get(url) as response:
                                   data = await response.json()
                                   break
                         except:
                              continue
                    else:
                         return HttpError
                    
                    results: list[dict[str, Any]] = data.get("results") 
                    if not results:
                         return SkinNotFoundError
                    
                    skins = [
                         SkinModel(
                              name=item.get("asset_description").get("market_hash_name"),
                              avatar=self.icon_url + item.get("asset_description").get("icon_url"),
                              price=float(item.get("sell_price_text")[1:].replace(",", ""))
                         ).model_dump()
                         for item in results
                    ]
                    await redis_session.set(
                         name=key,
                         value=json.dumps(skins),
                         ex=1000
                    )
          return skins
     
     
     async def skin_exists(
          self,
          skin_name: str
     ) -> AbstractResponse | SkinModel:
          url = f"https://steamfolio.com/Item/GetReactModel?name={skin_name.replace('&', '%26')}"
          
          async with aiohttp.ClientSession() as session:
               for _ in range(3):
                    try:
                         async with session.get(url) as response:
                              if response.status == 400:
                                   return SkinNotFoundError
                              data = await response.json()
                              item = data["data"]["item"]
                              break
                    except:
                         continue
               else:
                    return HttpError
               return SkinModel(
                    name=item.get("marketHashName"),
                    avatar=item.get("image"),
                    price=round(item.get("safePrice"), 2)
               )
               
               
     async def skin_price_history(
          self,
          skin_name: str
     ) -> list[dict[str, Any]]:
          async with aiohttp.ClientSession() as session:
               url = f"https://steamfolio.com/api/Graph/itemChart?name={skin_name.replace('&', '%26')}"
               for _ in range(3):
                    try:
                         async with session.get(url) as response:
                              json_data = await response.json()
                              data = json_data["data"]["all"]["values"]
                              volume = json_data["data"]["all"]["volumes"]
                              break
                    except:
                         continue
               else:
                    return HttpError
               
          
          price_history = []
          for index, part in enumerate(data):
               time = part["time"]
               if isinstance(time, int):
                    time = datetime.fromtimestamp(time)
                         
               elif isinstance(time, str):
                    time = datetime.fromisoformat(time)
                    
               price_history.append(
                    {
                         "item_id": uuid.uuid4(),
                         "skin_name": skin_name,
                         "price": round(float(part["value"]), 2),
                         "volume": volume[index]["value"],
                         "timestamp": time
                    }
               )
          return price_history
     
     
     async def get_skin_price(self, skin_name: str) -> tuple[float, int]:
          url = (
               "https://steamcommunity.com/market/"
               f"priceoverview/?currency=1&appid=730&market_hash_name={skin_name.replace('&', '%26')}"
          )
          async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                    if response.status == 403:
                         return HttpError
                    data = await response.json()
                    
          price = data.get("lowest_price")
          if price is None:
               price = data.get("median_price")
               if price is None:
                    return HttpError
          
          volume = data.get("volume")
          if volume is None:
               return HttpError
          
          # price = $0.50, volume = '101,456'
          return (float(price[1:])), int(volume.replace(",", ""))
               
               
               
               
               
               
               