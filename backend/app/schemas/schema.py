import json

from typing import Generic, TypeVar, Any, Type
from typing_extensions import Self
from datetime import datetime

from math import ceil
from pydantic import (
     BaseModel, 
     Field, 
     ConfigDict,
     model_validator,
)

from app.repositories.abc_condition import BaseWhereCondition
from .enums import (
     OrderByModeEnum, 
     OrderByPaginateSkinsEnum, 
     UserNotifyEnum, 
     WhereConditionEnum,
     NotifyTypeEnum,
     OrderByPaginatePortfolioSkinsEnum
)



SKIN_ON_PAGE = TypeVar("SKIN_ON_PAGE", bound=BaseModel)

        
        
class _NullableValue(BaseModel):
     def non_nullable(self, exclude: list[str] = []) -> dict[str, Any]:
          return {
               key: value
               for key, value in self.__dict__.items()
               if (value is not None) and (key not in exclude)
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
     
     
     def generate_conditions(
          self,
          attrs_conditions: dict[str, list[str, WhereConditionEnum]],
          condition: Type[BaseWhereCondition],
          additional_conditions: list[BaseWhereCondition] = [],
          exclude: list[str] = []
     ) -> list[BaseWhereCondition]:
          non_nullable = self.non_nullable(exclude=exclude)
          instance_conditions = [
               condition(attrs_conditions[attr][0], value, attrs_conditions[attr][1]) 
               for attr, value in non_nullable.items()
               if attrs_conditions.get(attr, None)
          ]
          if additional_conditions:
               instance_conditions.extend(additional_conditions)
          return instance_conditions
     
     
class _PatchModel(BaseModel):
     def get_update_field_values(self) -> dict[str, Any]:
          return {
               key: value
               for key, value in self.__dict__.items() if value is not None
          }
     


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

     
class PatchUserModel(_PatchModel):
     notify: UserNotifyEnum | None = Field(default=None)
     
     model_config = ConfigDict(use_enum_values=True)    
     
     
class PatchPortfolioSkinModel(_PatchModel):
     notify_percent: int | None = Field(default=None, ge=1) 
     
     
          
class PaginateSkinsModel(_NullableValue):
     query: str | None = Field(default=None)
     limit: int = Field(default=10, ge=1, le=20)
     offset: int = Field(default=0, ge=0)
     price_min: float | None = Field(default=None, ge=0)
     price_max: float | None = Field(default=None, ge=0)
     category: str | None = Field(default=None)
     weapon: str | None = Field(default=None)
     wear: str | None = Field(default=None)
     rarity: str | None = Field(default=None)
     stattrak: bool | None = Field(default=None)
     souvenir: bool | None = Field(default=None)
     collection: str | None = Field(default=None)
     order_by: OrderByPaginateSkinsEnum = Field(default=OrderByPaginateSkinsEnum.POPULAR)
     order_by_mode: OrderByModeEnum = Field(default=OrderByModeEnum.DESC)
     
     model_config = ConfigDict(use_enum_values=True)
     
     
     def generate_conditions(
          self, 
          condition: Type[BaseWhereCondition],
          additional_conditions: list[BaseWhereCondition] = [],
          exclude: list[str] = []
     ) -> list[BaseWhereCondition]:
          attrs_conditions = {
               "query": ["market_hash_name", WhereConditionEnum.ILIKE],
               "price_min": ["price", WhereConditionEnum.GE],
               "price_max": ["price", WhereConditionEnum.LE],
               "category": ["category", WhereConditionEnum.EQ],
               "weapon": ["weapon", WhereConditionEnum.EQ],
               "wear": ["wear", WhereConditionEnum.EQ],
               "rarity": ["rarity", WhereConditionEnum.EQ],
               "stattrak": ["stattrak", WhereConditionEnum.EQ],
               "souvenir": ["souvenir", WhereConditionEnum.EQ],
          }
          return super().generate_conditions(
               attrs_conditions=attrs_conditions,
               condition=condition,
               additional_conditions=additional_conditions,
               exclude=exclude
          )          
          
          
class PaginareSkinsPortfolioModel(PaginateSkinsModel):
     order_by: OrderByPaginatePortfolioSkinsEnum = Field(
          default=OrderByPaginatePortfolioSkinsEnum.BENEFIT
     )
     
     
     
class CreateSkinTransactionModel(BaseModel):
     buy_price: float = Field(default=0, ge=0)
     count: int = Field(default=1, ge=1)
     when_buy: datetime = Field(default_factory=lambda: datetime.now())
     
     
class PatchSkinTransactionModel(_PatchModel):
     buy_price: float | None = Field(default=None, ge=0)
     count: int | None = Field(default=None, ge=1)
     when_buy: datetime | None = Field(default=None)
     
     
class NotifyFiltersModel(_NullableValue):
     is_read: bool | None = Field(default=None)
     notify_type: NotifyTypeEnum | None = Field(default=None)
     
     model_config = ConfigDict(use_enum_values=True)
     
     def generate_conditions(
          self,
          condition: Type[BaseWhereCondition],
          additional_conditions: list[BaseWhereCondition] = [],
          exclude: list[str] = []
     ) -> list[BaseWhereCondition]:
          attrs_conditions = {
               "is_read": ["is_read", WhereConditionEnum.EQ],
               "notify_type": ["notify_type", WhereConditionEnum.EQ]
          }
          return super().generate_conditions(
               attrs_conditions=attrs_conditions,
               condition=condition,
               additional_conditions=additional_conditions,
               exclude=exclude
          )