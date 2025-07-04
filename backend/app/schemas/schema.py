from uuid import UUID
from typing import TypeVar, Any
from datetime import datetime
from pydantic import BaseModel



T = TypeVar("T")



class UserModel(BaseModel):
     uuid: UUID | str
     steam_id: int
     steam_name: str
     steam_avatar: str
     created_at: datetime
     telegram_id: int | None = None
     telegram_username: str | None = None
     
     def model_post_init(self, _: Any) -> None:
         self.uuid = str(self.uuid)




class SkinModel(BaseModel):
     id: str | None = None
     name: str
     avatar: str
     price: float
     price_last_1_day: float | None = None
     price_last_30_day: float | None = None
     price_last_365_day: float | None = None
     
     


class SkinPriceHistoryModel(BaseModel):
     item_id: int
     skin_id: str
     skin_name: str
     volume: int
     price: float
     timestamp: datetime
     


class SkinHistoryModel(BaseModel):
     price: float
     volume: int
     timestamp: str
     
     
     
class SkinHistoryTimePartModel(BaseModel):
     all: list["SkinHistoryModel"]
     year: list["SkinHistoryModel"]
     month: list["SkinHistoryModel"]
     day: list["SkinHistoryModel"]
     
     

class UserPortfolioModel(BaseModel):
     item_id: int
     skin_id: str
     user_uuid: str
     quantity: int
     buy_price: float
     
     
     
     
class UserRelModel(UserModel):
     portfolio: list["UserPortfolioModel"]
     
   
     
class SkinRelModel(SkinModel):
     history: list["SkinPriceHistoryModel"]
     
    
          
class TokenPayload(BaseModel):
     uuid: str
     iat: datetime
     exp: datetime
     
     
class SteamItem(BaseModel):
     name: str
     avatar: str
     quantity: int
     