from uuid import UUID
from typing import Generic, TypeVar
from datetime import datetime
from pydantic import BaseModel



T = TypeVar("T")



class UserModel(BaseModel):
     uuid: UUID
     steam_id: int
     steam_name: str
     steam_avatar: str
     created_at: datetime
     telegram_id: int | None = None
     telegram_username: str | None = None



class SkinModel(BaseModel):
     id: int
     name: str
     avatar: str
     price: float
     rarity: str | None
     category: str | None
     collection: str | None
     skin_type: str | None
     price_last_1_day: float
     price_last_7_days: float
     price_last_30_days: float     
     
     


class SkinPriceHistoryModel(BaseModel):
     id: int
     name: str
     price: float
     timestamp: datetime
     
     

class UserPortfolioModel(BaseModel):
     item_id: int
     skin_id: int
     user_uuid: str
     quantity: int
     buy_price: float
     
     
     
class UserPortfolioRelModel(UserPortfolioModel):
     user: "UserModel"
     
     
     
class UserRelModel(UserModel):
     portfolio: list["UserPortfolioModel"]
     
     
    
          
class TokenPayload(BaseModel):
     uuid: str
     iat: datetime
     exp: datetime
     
     
     
     
class SteamItem(BaseModel):
     name: str
     avatar: str
     rarity: str | None
     collection: str | None
     skin_type: str | None
     quantity: int
     
     
     
class EndpointResponse(BaseModel, Generic[T]):
     detail: T
     