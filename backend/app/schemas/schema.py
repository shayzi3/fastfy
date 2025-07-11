from uuid import UUID
from typing import  Any
from datetime import datetime
from pydantic import BaseModel

from .enums import UpdateMode






class UserModel(BaseModel):
     uuid: UUID | str
     steam_id: int
     steam_name: str
     steam_avatar: str
     created_at: datetime
     skin_percent: int
     telegram_id: int | None = None
     telegram_username: str | None = None
     
     def model_post_init(self, _: Any) -> None:
         self.uuid = str(self.uuid)




class SkinModel(BaseModel):
     name: str
     avatar: str
     price: float
     update_mode: UpdateMode | None = None
     price_last_1_day: float | None = None
     price_last_30_day: float | None = None
     price_last_365_day: float | None = None
     
     

class SkinPriceHistoryModel(BaseModel):
     item_id: UUID | str
     skin_name: str
     volume: int
     price: float
     timestamp: datetime
     
     
     def model_post_init(self, _: Any) -> None:
          self.item_id = str(self.item_id)
          
     


class UserPortfolioModel(BaseModel):
     item_id: UUID | str
     user_uuid: UUID | str
     skin_name: str
     quantity: int
     buy_price: float  
     
     
     def model_post_init(self, _: Any) -> None:
         self.user_uuid = str(self.user_uuid)   
         self.item_id = str(self.item_id)
         
         
         
class UserNotifyModel(BaseModel):
     notify_id: UUID | str
     user_uuid: UUID | str
     text: str
     created_at: datetime
     is_read: bool
     
     def model_post_init(self, _: Any):
         self.notify_id = str(self.notify_id)
         self.user_uuid = str(self.user_uuid)



class UserRelModel(UserModel):
     portfolio: list["UserPortfolioModel"]
          
     
     
class UserPortfolioRelModel(UserPortfolioModel):
     skin: "SkinModel"




class SkinHistoryModel(BaseModel):
     price: float
     volume: int
     timestamp: str
     
     
     
     
class SkinHistoryTimePartModel(BaseModel):
     all: list["SkinHistoryModel"]
     year: list["SkinHistoryModel"]
     month: list["SkinHistoryModel"]
     day: list["SkinHistoryModel"]
     
          
          
class TokenPayload(BaseModel):
     uuid: str
     iat: datetime
     exp: datetime
     
     
     
class SteamItem(BaseModel):
     name: str
     avatar: str
     quantity: int
     