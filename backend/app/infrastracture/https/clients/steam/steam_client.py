import json

from app.responses import SteamInventoryBlockedError
from app.schemas import (
     SteamInventorySkinModel, 
     SkinsPage, 
     SkinPriceVolumeModel, 
     RepeatRequestModel,
     SteamUserModel
)
from backend.app.infrastracture.https.http_clients.abc import BaseHttpClient
from .abc import BaseSteamClient
from backend.app.responses.abc import BaseResponse
from backend.app.infrastracture.cache.abc import Cache
from app.infrastracture.https.repeater import retry
from app.core import my_config
from app.utils.logger import logger



class SteamClient(BaseSteamClient):
     def __init__(self, http_client: BaseHttpClient):
          self.http_client = http_client
          self.image_link = ""
          
     
     @retry(max_attemps=3, delay=2, log_category="http_steam")
     async def get_steam_profile(
          self, 
          steam_id: int, 
     ) -> SteamUserModel | RepeatRequestModel:
          response = await self.http_client.request(
               method="GET",
               url="https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/",
               query_arguments={
                    "key": my_config.steam_api_key,
                    "steamids": steam_id
               }
          )
          if isinstance(response, RepeatRequestModel):
               return response
          
          data = response.dict_format()
          response_data = data.get("response")
          if "players" in response_data and response_data.get("players"):
               players = response_data.get("players")[0]
               return SteamUserModel(
                    steam_name=players.get("personaname"),
                    steam_avatar=players.get("avatarmedium")
               )
          
          return RepeatRequestModel(
               status_code=response.status_code,
               text=response.text
          )
               
          
     @retry(max_attemps=3, delay=15, log_category="http_steam")
     async def get_steam_inventory(
          self, 
          steamid: int, 
          cache: Cache,
          offset: int,
          limit: int,
     ) -> SkinsPage[SteamInventorySkinModel] | BaseResponse:
          skins = await cache.get(f"steam_inventory:{steamid}")
          if skins is not None:
               data = json.loads(skins)
               return SkinsPage(
                    pages=len(data),
                    current_page=offset,
                    skins=[
                         SteamInventorySkinModel.model_validate(json.loads(model))
                         for model in data[offset:limit + offset]
                    ],
                    skins_on_page=limit
               ).serialize_pages()
               
               
          response = await self.http_client.request(
               method="GET",
               url=f"https://steamcommunity.com/inventory/{steamid}/730/2"
          )
          if isinstance(response, RepeatRequestModel):
               return response
          
          elif response.status_code in [401, 403]:
               # Profile incognito, invetory incognito, inventory empty, User unauthorized
               return SteamInventoryBlockedError
               
          data = response.dict_format()
          
          inventory = []
          descriptions = data.get("descriptions", [])
          for inventory_item in descriptions:
               if inventory_item.get("marketable") == 1:
                    skin_name = inventory_item["market_hash_name"]
                    if skin_name not in inventory:
                         inventory.append(
                              SteamInventorySkinModel(
                                   market_hash_name=inventory_item.get("market_hash_name", ""),
                                   image_link=self.image_link + inventory_item.get("icon_url", "")
                              )
                         )
          if skins:
               await cache.set(
                    name=f"steam_inventory:{steamid}",
                    value=json.dumps([skin.model_dump_json() for skin in skins]),
                    ex=7200
               )
          return SkinsPage(
               pages=len(skins),
               current_page=offset,
               skins=skins[offset:limit + offset],
               skins_on_page=limit
          ).serialize_pages()
     
     
     @retry(max_attemps=10, delay=20, log_category="http_steam")
     async def get_skin_price(
          self, 
          skin_name: str, 
     ) -> SkinPriceVolumeModel | RepeatRequestModel:
          response = await self.http_client.request(
               method="GET",
               url="https://steamcommunity.com/market/priceoverview/",
               query_arguments={
                    "currency": 1,
                    "appid": 730,
                    "market_hash_name": skin_name
               }
          )
          if isinstance(response, RepeatRequestModel):
               return response
          
          data = response.dict_format()
          price = data.get("lowest_price")
          if price is None:
               price = data.get("median_price")
               if price is None:
                    logger.http_steam.error(msg=f"{response.status_code} {response.text}")
                    return RepeatRequestModel(
                         status_code=response.status_code,
                         text=response.text
                    )
          
          volume = data.get("volume")
          if volume is None:
               logger.http_steam.error(msg=f"{response.status_code} {response.text}")
               return RepeatRequestModel(
                    status_code=response.status_code,
                    text=response.text
               )
          return SkinPriceVolumeModel(price=price, volume=volume)
          
               
               
               
               
               
               
               