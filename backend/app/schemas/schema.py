from __future__ import annotations

import json

from math import ceil
from uuid import UUID
from typing import  Any
from datetime import datetime
from pydantic import BaseModel

from .enums import UpdateMode, NotifyType






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
          self.image = (
               "https://community.fastly.steamstatic.com"
               "/economy/image/" + self.image
          )


     
class SkinPriceInfoModel(BaseModel):
     skin_name: str
     update_mode: UpdateMode
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
          self.item_id = str(self.item_id)
          
     


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
     notify_type: NotifyType
     created_at: datetime
     is_read: bool
     
     def model_post_init(self, _: Any):
         self.uuid = str(self.uuid)
         self.user_uuid = str(self.user_uuid)
         
      
         
class UserNotifyRelModel(BaseModel):
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
     
     

     
     
class SkinsPage(BaseModel):
     pages: int
     current_page: int
     skins: list[Any]
     skin_model_obj: Any # parent class BaseModel
     
     
     def model_post_init(self, _: Any):
          self.current_page = (
               1 if self.current_page == 0
               else (self.current_page // 5) + 1
          )
          self.pages = ceil(self.pages / 5)
          
          if len(self.skins) > 0:
               if isinstance(self.skins[0], str):
                    self.skins = [
                         self.skin_model_obj.model_validate(json.loads(model))
                         for model in self.skins
                    ]   
               
class TokenPayload(BaseModel):
     uuid: str
     iat: datetime
     exp: datetime
     
     
class SteamItem(BaseModel):
     name: str
     avatar: str     
     
     

     