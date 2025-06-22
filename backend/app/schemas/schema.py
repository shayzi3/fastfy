from uuid import UUID
from datetime import datetime
from pydantic import BaseModel



class UserModel(BaseModel):
     uuid: UUID
     steam_id: int
     steam_name: str
     steam_avatar: str
     created_at: datetime
     telegram_id: int | None = None
     telegram_username: str | None = None



class SkinModel(BaseModel):
     skin_id: int
     skin_name: str
     skin_avatar: str
     skin_price: float
     rarity: str
     collection: str
     item_type: str
     price_last_1_day: float
     price_last_7_days: float
     price_last_30_days: float     
     
     


class SkinPriceHistoryModel(BaseModel):
     skin_id: int
     skin_name: str
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