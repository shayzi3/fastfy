from __future__ import annotations

from typing import Generic, TypeVar, Type, Literal
from typing_extensions import Self

from math import ceil
from uuid import UUID
from typing import  Any
from datetime import datetime
from pydantic import BaseModel, Field



SKIN_ON_PAGE = TypeVar("SKIN_ON_PAGE", bound=BaseModel)



class UserModel(BaseModel):
     uuid: UUID | str
     steam_id: int
     steam_name: str
     steam_avatar: str
     telegram_id: int | None = None
     telegram_username: str | None = None
     skin_percent: int
     created_at: datetime
     
     def model_post_init(self, _: Any) -> None:
         self.uuid = str(self.uuid)



class SkinModel(BaseModel):
     name: str
     image: str
     skin_price_info: SkinPriceInfoModel | None
     
     
     def model_post_init(self, _: Any):
          if "steamstatic" not in self.image:
               self.image = (
                    "https://community.fastly.steamstatic.com"
                    "/economy/image/" + self.image
               )


     
class SkinPriceInfoModel(BaseModel):
     skin_name: str
     update_mode: Literal["HIGH", "MEDIUM_WELL", "MEDIUM", "LOW"]
     last_update: datetime | None = None
     price: float | None = None
     price_last_1_day: float | None = None
     price_last_30_day: float | None = None
     price_last_365_day: float | None = None
     
          
     

class SkinPriceHistoryModel(BaseModel):
     uuid: UUID | str
     skin_name: str
     volume: int
     price: float
     timestamp: datetime
     
     def model_post_init(self, _: Any) -> None:
          self.uuid = str(self.uuid)
          
     


class UserSkinModel(BaseModel):
     uuid: UUID | str
     user_uuid: UUID | str
     skin_name: str
     
     
     def model_post_init(self, _: Any) -> None:
         self.uuid = str(self.uuid)
         self.user_uuid = str(self.user_uuid) 
         
         
class UserSkinRelModel(UserSkinModel):
     skin: SkinModel
     user: UserModel
         
         
class UserNotifyModel(BaseModel):
     uuid: UUID | str
     user_uuid: UUID | str
     text: str
     notify_type: Literal["SKIN", "INFO"]
     created_at: datetime
     is_read: bool
     
     def model_post_init(self, _: Any):
         self.uuid = str(self.uuid)
         self.user_uuid = str(self.user_uuid)
         
      
         
class UserNotifyRelModel(UserNotifyModel):
     user: UserModel



class SkinHistoryModel(BaseModel):
     price: float
     volume: int
     timestamp: str
     
     

class SkinHistoryTimePartModel(BaseModel):
     all: list[SkinHistoryModel]
     year: list[SkinHistoryModel]
     month: list[SkinHistoryModel]
     day: list[SkinHistoryModel]
     
     

     

class SkinsPage(BaseModel, Generic[SKIN_ON_PAGE]):
     pages: int
     current_page: int # offset
     skins: list[SKIN_ON_PAGE]
     skins_on_page: int = Field(exclude=True, default=5) # limit
     
     def serialize_pages(self) -> Self:
          self.current_page = (self.current_page // self.skins_on_page) + 1
          self.pages = ceil(self.pages / self.skins_on_page)   
          return self
     
          
               

class SteamItem(BaseModel):
     name: str
     avatar: str
     
     
     
class SkinPriceVolume(BaseModel):
     price: str | float
     volume: str | int
     
     
     def model_post_init(self, _: Any):
          self.volume = int(self.volume.replace(",", "")) # 1,456 -> 1456
          self.price = float(self.price.split()[0].replace(",", ".")) # 1249,50 руб -> 1249.50
     
     

     