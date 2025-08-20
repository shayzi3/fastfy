import json
import httpx
import asyncio

from fake_useragent import UserAgent

from app.infrastracture.redis import RedisPool
from app.core import my_config
from app.responses.abstract import AbstractResponse
from app.responses import HttpError, SteamInventoryBlocked
from app.schemas import SteamItem, SkinsPage, SkinPriceVolume
from app.logger import logger




class HttpSteamClient:
     def __init__(self):
          self.ua = UserAgent(platforms=["desktop"])
          self.icon_url = "https://community.akamai.steamstatic.com/economy/image/"
          
          
     def headers(self) -> dict[str, str]:
          return {
               "User-Agent": self.ua.random,
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Connection": "keep-alive"
          }
     
     
     async def get_steam_profile(
          self, 
          steam_id: int, 
          time: int = 0,
          mode: str = "request"
     ) -> tuple[str, str] | AbstractResponse:
          await asyncio.sleep(time)
          
          url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
          async with httpx.AsyncClient() as session:
               try:
                    response = await session.get(
                         url=url,
                         params={
                              "key": my_config.steam_api_key,
                              "steamids": steam_id
                         },
                         headers=self.headers()
                    )
                    data = await response.json()
               except Exception as ex:
                    if mode == "request":
                         return await self.get_steam_profile(
                              steam_id=steam_id,
                              time=5,
                              mode="reload"
                         )
                    else:
                         logger.http_steam.error(
                              msg=f"{response.status_code} {response.text}", 
                              exc_info=True
                         )
                         return HttpError
               
               response_data = data.get("response")
               if "players" in response_data and response_data.get("players"):
                    players = response_data.get("players")[0]
                    return (players.get("personaname"), players.get("avatarmedium"))
               
               logger.http_steam.error(msg=f"{response.status_code} {response.text}")
               return HttpError
               
          
     async def get_steam_inventory(
          self, 
          steamid: int, 
          redis_session: RedisPool,
          offset: int,
          limit: int,
          time: int = 0,
          mode: str = "request"
     ) -> SkinsPage | AbstractResponse:
          skins = await redis_session.get(f"steam_inventory:{steamid}")
          if skins is not None:
               models = json.loads(skins)
               return SkinsPage(
                    pages=len(models),
                    current_page=offset,
                    skins=models[offset:limit + offset],
                    skin_model_obj=SteamItem,
                    skins_on_page=limit
               )
               
          await asyncio.sleep(time)
               
          url = f"https://steamcommunity.com/inventory/{steamid}/730/2"
          async with httpx.AsyncClient() as session:
               try:
                    response = await session.get(url=url, headers=self.headers())
                    if response.status_code in [401, 403]:
                         # Profile incognito, invetory incognito, inventory empty, User unauthorized
                         return SteamInventoryBlocked
                         
                    data = response.json()
               except Exception as ex:
                    if mode == "request":
                         return await self.get_steam_inventory(
                              steamid=steamid,
                              redis_session=redis_session,
                              offset=offset,
                              limit=limit,
                              mode="reload",
                              time=5
                         )
                    else:
                         logger.http_steam.error(
                              msg=response.status_code, 
                              exc_info=True
                         )
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
                    ex=7200
               )
          return SkinsPage(
               pages=len(skins),
               current_page=offset,
               skins=skins[offset:limit + offset],
               skin_model_obj=SteamItem,
               skins_on_page=limit
          )
     
     
     async def get_skin_price(
          self, 
          skin_name: str, 
          time: int = 0
     ) -> SkinPriceVolume | AbstractResponse:
          if time >= 60:
               time = 0
          
          await asyncio.sleep(time)
          
          url = "https://steamcommunity.com/market/priceoverview/"
          async with httpx.AsyncClient() as session:
               try:
                    response = await session.get(
                         url=url,
                         params={
                              "currency": 5,
                              "appid": 730,
                              "market_hash_name": skin_name
                         },
                         headers=self.headers()
                    )
                    data = await response.json()
               except:
                    return await self.get_skin_price(
                         skin_name=skin_name,
                         time=time + 2
                    )
                    
          price = data.get("lowest_price")
          if price is None:
               price = data.get("median_price")
               if price is None:
                    logger.http_steam.error(msg=f"{response.status_code} {response.text}")
                    return HttpError
          
          volume = data.get("volume")
          if volume is None:
               logger.http_steam.error(msg=f"{response.status_code} {response.text}")
               return HttpError
          return SkinPriceVolume(price=price, volume=volume)
          
               
               
               
               
               
               
               