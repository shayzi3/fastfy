import aiohttp
import json

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
               try:
                    result = await session.get(url)
                    data: dict[str, dict[str, list[dict]]] = await result.json()
               except:
                    return HttpError
               
               response = data.get("response")
               if "players" in response and response.get("players"):
                    players = response.get("players")[0]
                    return (players.get("personaname"), players.get("avatarmedium"))
               return HttpError
               
               
     async def get_steam_inventory(self, steamid: int) -> list[SteamItem] | AbstractResponse:
          url = f"https://steamcommunity.com/inventory/{steamid}/730/2"
          
          async with aiohttp.ClientSession() as session:
               try:
                    result = await session.get(url)
                    
                    # errors
                     
                    data = await result.json()
               except:
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
                              response = await session.get(url)
                              data = await response.json()
                              break
                         except:
                              continue
                    
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
          
               
               
               
               
               
               
               
               