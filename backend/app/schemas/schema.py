import json

from typing import Generic, TypeVar, Any
from typing_extensions import Self
from datetime import datetime

from math import ceil
from pydantic import (
     BaseModel, 
     Field, 
     ConfigDict,
     model_validator
)

from .enums import OrderByModeEnum, OrderByPaginateSkinsEnum, UserNotifyEnum



SKIN_ON_PAGE = TypeVar("SKIN_ON_PAGE", bound=BaseModel)

        
        
class _NullableValue(BaseModel):
     model_config = ConfigDict(use_enum_values=True)
     
     def non_nullable(self, exclude: list[str] = []) -> dict[str, Any]:
          return {
               key: value
               for key, value in self.__dict__.items()
               if value is not None and key not in exclude
          }  
          
     @model_validator(mode="after")
     def validator(self) -> Self:
          if all([hasattr(self, attr) for attr in ["limit", "offset"]]):
               if self.offset % self.limit != 0:
                    raise ValueError("The offset parameter must be divisible by limit without remainder.")
          return self
     
     def cache_key(self, prefix: str, exclude: list[str] = []) -> str:
          non_nullable_values = self.non_nullable(exclude)
          return f"{prefix}:" + "~".join([f"{key}={value}" for key, value in non_nullable_values])
       

class SkinPriceHistoryModel(BaseModel):
     price: float
     volume: int
     timestamp: str
     
     

class SkinHistoryTimePartModel(BaseModel):
     all: list[SkinPriceHistoryModel]
     year: list[SkinPriceHistoryModel]
     month: list[SkinPriceHistoryModel]
     week: list[SkinPriceHistoryModel]
     day: list[SkinPriceHistoryModel]
     
     

class SkinsPage(BaseModel, Generic[SKIN_ON_PAGE]):
     pages: int
     current_page: int # offset
     skins: list[SKIN_ON_PAGE]
     skins_on_page: int = Field(exclude=True, default=5) # limit
     
     def serialize(self) -> Self:
          self.current_page = (self.current_page // self.skins_on_page) + 1
          self.pages = ceil(self.pages / self.skins_on_page)
          return self
     
               

class SteamInventorySkinModel(BaseModel):
     market_hash_name: str
     image_link: str
     
     
class TelegramDataModel(BaseModel):
     telegram_username: str
     telegram_id: int
     

class SteamProfileModel(BaseModel):
     steamid: int
     steam_name: str
     steam_avatar: str
          
     
class SkinPriceVolumeModel(BaseModel):
     price: str | float
     volume: str | int
     
     def serialize(self) -> Self:
          self.volume = int(self.volume.replace(",", "")) # 1,456 -> 1456
          self.price = float(self.price.split()[0].replace(",", ".")) # 1249,50 руб -> 1249.50
          return self
     
     
class HttpResponseModel(BaseModel):
     status_code: int
     text: str
     
     def dict_format(self) -> dict[str, Any]:
          return json.loads(self.text)
     
     
     
class RepeatRequestModel(BaseModel):
     status_code: str
     text: str
     

     
class SteamUserModel(BaseModel):
     steam_name: str
     steam_avatar: str
     

     
class JWTTokenPayloadModel(BaseModel):
     uuid: str
     steam_name: str
     steam_avatar: str
     steam_id: int
     iat: datetime
     exp: datetime
     
     
     
class ExchangeKeyModel(BaseModel):
     exchange_key: str
     
     
class AccessTokenModel(BaseModel):
     access_token: str
     
     
     
class PatchUserModel(_NullableValue):
     notify: UserNotifyEnum | None = Field(default=None)
     
          
          
class PaginateSkinsModel(_NullableValue):
     query: str | None = Field(default=None)
     limit: int = Field(ge=1, le=20)
     offset: int = Field(ge=0)
     category: str | None = Field(default=None)
     weapon: str | None = Field(default=None)
     wear: str | None = Field(default=None)
     rarity: str | None = Field(default=None)
     stattrak: bool = Field(default=False)
     souvenir: bool = Field(default=False)
     order_by: OrderByPaginateSkinsEnum | None = Field(default=None)
     order_by_mode: OrderByModeEnum | None = Field(default=None)
     metas: bool = Field(default=True)
     
     
class PaginatePortfolioSkinsModel(_NullableValue):
     limit: int = Field(ge=1, le=20)
     offset: int = Field(ge=0)


class PaginateUserLikeSkinsModel(_NullableValue):
     limit: int = Field(ge=1, le=20)
     offset: int = Field(ge=0)
     
     
class SkinWithoutMetasModel(BaseModel):
     market_hash_name: str
     color: str
     image_link: str
     
     
class CreateSkinTransactionModel(BaseModel):
     buy_price: float = Field(ge=0)
     count: int = Field(ge=1)
     when_buy: datetime | None = Field(default=None)
     
     
class UpdateSkinTransactionModel(_NullableValue):
     buy_price: float | None = Field(default=None, ge=0)
     count: int | None = Field(default=None, ge=1)
     when_buy: datetime | None = Field(default=None)
     