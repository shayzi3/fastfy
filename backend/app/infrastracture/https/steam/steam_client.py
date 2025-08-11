import json
import aiohttp


from app.infrastracture.redis import RedisPool
from app.core import my_config
from app.responses.abstract import AbstractResponse
from app.responses import HttpError, SteamInventoryBlocked
from app.schemas import SteamItem, SkinsPage




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
               
           
     async def get_steam_inventory(
          self, 
          steamid: int, 
          redis_session: RedisPool,
          offset: int
     ) -> SkinsPage | AbstractResponse:
          skins = await redis_session.get(f"steam_inventory:{steamid}")
          if skins is not None:
               models = json.loads(skins)
               return SkinsPage(
                    pages=len(models),
                    current_page=offset,
                    skins=models[offset:5 + offset],
                    skin_model_obj=SteamItem
               )
               
          url = f"https://steamcommunity.com/inventory/{steamid}/730/2"
          async with aiohttp.ClientSession() as session:
               for _ in range(3):
                    try:
                         async with session.get(url) as response:
                              if response.status in [401, 403]:
                                   # Profile incognito, invetory incognito, inventory empty, User unauthorized
                                   return SteamInventoryBlocked
                              
                              data = await response.json()
                              break
                    except:
                         continue
               else:
                    return HttpError
               
               descriptions = data.get("descriptions")
               inventory = set()
               for inventory_item in descriptions:
                    if inventory_item.get("marketable") == 1:
                         inventory.add(
                              (
                                   inventory_item.get("market_hash_name"),
                                   self.icon_url + inventory_item.get("icon_url")
                              )
                         )
                         
          skins = [SteamItem(name=name, avatar=image) for name, image in inventory]
          if skins:
               await redis_session.set(
                    name=f"steam_inventory:{steamid}",
                    value=json.dumps([skin.model_dump_json() for skin in skins]),
                    ex=1200
               )
          return SkinsPage(
               pages=len(skins),
               current_page=offset,
               skins=skins[offset:5 + offset],
               skin_model_obj=SteamItem
          )
     
     
     async def get_skin_price(self, skin_name: str) -> tuple[float, int]:
          url = (
               "https://steamcommunity.com/market/"
               f"priceoverview/?currency=1&appid=730&market_hash_name={skin_name.replace('&', '%26')}"
          )
          async with aiohttp.ClientSession() as session:
               async with session.get(url) as response:
                    if response.status != 200:
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
               
               
               
               
               
               
               