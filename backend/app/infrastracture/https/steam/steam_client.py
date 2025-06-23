import aiohttp

from app.core import my_config
from app.responses.abstract import AbstractResponse
from app.responses import HttpError
from app.schemas import SteamItem




class HttpSteamClient:
     def __init__(self):
          self.base_url = "https://api.steampowered.com"
          self.api_key = my_config.steam_api_key
     
     
     async def get_steam_profile(self, steamids: int) -> tuple[str, str] | AbstractResponse:
          url = (
               self.base_url + 
               "/ISteamUser/GetPlayerSummaries/v0002/" +
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
          icon_url = "https://community.akamai.steamstatic.com/economy/image/"
          
          async with aiohttp.ClientSession() as session:
               try:
                    result = await session.get(url)
                    
                    if result.status == 401:
                         ...
                         
                    data = await result.json()
               except:
                    return HttpError
               
               assets = data.get("assets")
               descriptions = data.get("descriptions")
               
               count_skins = {}
               for item in assets:
                    if item.get("classid") not in count_skins.keys():
                         count_skins[item.get("classid")] = 0
                    count_skins[item.get("classid")] += 1
                    
               inventory = []
               for inventory_item in descriptions:
                    if inventory_item.get("marketable") == 1:
                         rarity, collection, skin_type, category = None, None, None, None
                         for types in inventory_item.get("tags"):
                              catalog = types.get("localized_category_name")
                              
                              if catalog == "Type":
                                   skin_type = types.get("localized_tag_name")
                                   
                              if catalog == "Collection":
                                   collection = types.get("localized_tag_name")
                                   
                              if catalog == "Quality":
                                   rarity = types.get("localized_tag_name")
                                   
                              if catalog == "Weapon":
                                   category = types.get("localized_tag_name")
                              
                         inventory.append(
                              SteamItem(
                                   name=inventory_item.get("market_hash_name"),
                                   avatar=icon_url + inventory_item.get("icon_url"),
                                   rarity=rarity,
                                   collection=collection,
                                   skin_type=skin_type,
                                   quantity=count_skins.get(inventory_item.get("classid"))
                              )
                         )
               return inventory
               
               
               
               
               
               
               
               