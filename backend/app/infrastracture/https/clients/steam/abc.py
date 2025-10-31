from typing import Protocol

from backend.app.responses.abc import BaseResponse
from backend.app.infrastracture.cache.abc import Cache
from app.schemas import SkinsPage, SteamItemModel, SkinPriceVolumeModel, RepeatRequestModel, SteamUserModel




class BaseSteamClient(Protocol):
     
     async def get_steam_profile(
          self, 
          steam_id: int
     ) -> SteamUserModel | RepeatRequestModel:
          ...
          
          
     async def get_steam_inventory(
          self,
          steamid: int, 
          cache: Cache,
          offset: int,
          limit: int,
     ) -> SkinsPage[SteamItemModel] | BaseResponse:
          ...
          
          
     async def get_skin_price(
          self,
          skin_name: str
     ) -> SkinPriceVolumeModel | RepeatRequestModel:
          ...