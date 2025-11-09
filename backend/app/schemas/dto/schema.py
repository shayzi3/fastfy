from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, model_validator, Field
from typing_extensions import Self, Literal



class Base(BaseModel):
     
     @model_validator(mode="before")
     def validator(self) -> Self:
          for key, item in self.__dict__.items():
               if isinstance(item, UUID):
                    setattr(self, key, str(item))
               
               

class UserDTO(Base):
     uuid: str
     steam_id: int
     steam_name: str
     steam_avatar: str
     telegram_id: int | None = None
     telegram_username: str | None = None
     created_at: datetime
     notify: bool
      

               
class SkinDTO(Base):
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
     last_price: float | None = None
     last_price_update: datetime | None = None
     sell_by_last_update: int
     
     collections: list["SkinCollectionDTO"] = []
               
     
     
class SkinPriceHistoryDTO(Base):
     uuid: str 
     market_hash_name: str
     volume: int
     price: float
     timestamp: datetime
     
               
     
class UserPortfolioDTO(Base):
     uuid: str
     user_uuid: str
     market_hash_name: str
     benefit: float
     notify_percent: int
     
     skin: SkinDTO
     user: UserDTO
     transations: list["PortfolioSkinTransactionDTO"] = []
     
               
               
class PortfolioSkinTransactionDTO(Base):
     uuid: str
     portfolio_skin_uuid: str
     count: int
     buy_price: float
     when_buy: datetime | None = None
     
     
class UserLikeSkinDTO(Base):
     uuid: str
     user_uuid: str
     market_hash_name: str
     skin: SkinDTO
     collections: list["SkinCollectionDTO"] = []
     
     
class UserNotifyDTO(Base):
     uuid: str
     user_uuid: str
     text: str
     notify_type: Literal["SKIN", "INFO"]
     created_at: datetime
     is_read: bool
     user: UserDTO
               
               
class SkinCollectionDTO(Base):
     uuid: str = Field(exclude=True)
     market_hash_name: str = Field(exclude=True)
     short_name: str = Field(exclude=True)
     collection: str
     image_link: str