from uuid import UUID
from datetime import datetime
from typing import Literal

from pydantic import BaseModel



class UserDTOPresentation(BaseModel):
     uuid: UUID
     steam_id: int
     steam_name: str
     steam_avatar: str
     telegram_id: int | None = None
     telegram_username: str | None = None
     created_at: datetime
     notify: bool  


class SkinDTOPresentation(BaseModel):
     market_hash_name: str
     short_name: str
     category: str
     weapon: str | None  
     wear: str | None
     rarity: str
     color: str
     stattrak: bool | None
     souvenir: bool | None
     image_link: str     
     price: float | None = None
     price_last_1_day: float | None = None
     price_last_7_day: float | None = None
     price_last_30_day: float | None = None
     price_last_365_day: float | None = None
     price_last_all_day: float | None = None
     last_price_update: datetime | None = None
     
     collections: list["SkinCollectionDTOPresentation"] = []
     


class SkinPriceHistoryDTOPresentation(BaseModel):
     volume: int
     price: float
     timestamp: datetime
     

class UserPortfolioDTOPresentation(BaseModel):
     uuid: UUID
     market_hash_name: str
     benefit: float
     notify_percent: int
     
     skin: SkinDTOPresentation
     transations: list["PortfolioSkinTransactionDTOPresentation"] = []
     
     
     
class PortfolioSkinTransactionDTOPresentation(BaseModel):
     uuid: UUID
     count: int
     comment: str
     buy_price: float
     when_buy: datetime | None = None
     
     
class UserLikeSkinDTOPresentation(BaseModel):
     uuid: UUID
     market_hash_name: str
     skin: SkinDTOPresentation
     
     
class UserNotifyDTOPresentation(BaseModel):
     uuid: UUID
     text: str
     notify_type: Literal["SKIN", "INFO"]
     created_at: datetime
     is_read: bool
               
               
class SkinCollectionDTOPresentation(BaseModel):
     short_name: str
     collection: str
     image_link: str