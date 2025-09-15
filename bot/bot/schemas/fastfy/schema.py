from typing import Any, TypeVar, Generic, Type
from datetime import datetime

from pydantic import BaseModel, model_validator
from aiogram.utils.text_decorations import markdown_decoration
from aiogram.utils.markdown import bold, code

from .enums import DetailStatus



SKINS_ON_PAGE = TypeVar("SKINS_ON_PAGE", bound=BaseModel)



class ResponseObjectSchema(BaseModel):
     status_code: int
     obj: dict[str, Any] | list[dict[str, Any]]


class DetailSchema(BaseModel):
     is_detail: bool = True
     status: DetailStatus
     detail: str
     
     
class _SkinPriceInfoSchema(BaseModel):
     skin_name: str
     update_mode: str
     last_update: str
     price: float | None
     price_last_1_day: float | None
     price_last_30_day: float | None
     price_last_365_day: float | None
     

     
class SkinSchema(BaseModel):
     name: str
     image: str
     skin_price_info: _SkinPriceInfoSchema | None
     
     
     def serialize_for_text(self) -> tuple[str, float, float, float]:
          return (
               datetime.fromisoformat(self.skin_price_info.last_update).
               strftime("%d %B %H:%M:%S %Y"),
               
               self.skin_price_info.price
               if self.skin_price_info.price 
               else 0,
               
               self.skin_price_info.price_last_1_day
               if self.skin_price_info.price_last_1_day
               else 0,
               
               self.skin_price_info.price_last_30_day
               if self.skin_price_info.price_last_30_day
               else 0
          )
          
     def to_text(self) -> str:
          last_update, price, last_1, last_30 = self.serialize_for_text()
          return (
               f"{bold(self.name)}"
               f"\n\nЦена за {code(last_update)}: {bold(str(price) + 'р')}"
               f"\nИзменение цены за 1 день: {bold(str(last_1) + '%')}"
               f"\nИзменение цены за 30 дней: {bold(str(last_30) + '%')}"
          )
     

     
class SkinsOnPageSchema(BaseModel, Generic[SKINS_ON_PAGE]):
     pages: int
     current_page: int
     skins: list[SKINS_ON_PAGE]
     skin_model: Type[SKINS_ON_PAGE]
     
     @model_validator(mode="before")
     def validator(data: dict[str, Any]) -> dict[str, Any]:
          skin_model: Type[SKINS_ON_PAGE] = data["skin_model"]
          data["skins"] = [
               skin_model.model_validate(skin_data)
               for skin_data in data["skins"]
          ]
          return data
          
          
class _HistorySchema(BaseModel):
     price: float
     volume: int
     timestamp: str
     
       
class SkinPriceHistorySchema(BaseModel):
     all: list[_HistorySchema]
     year: list[_HistorySchema]
     month: list[_HistorySchema]
     day: list[_HistorySchema]
     

     
class UserSchema(BaseModel):
     uuid: str
     steam_id: int
     steam_name: str
     steam_avatar: str
     telegram_id: int
     telegram_username: str
     skin_percent: int
     created_at: str
     
     
     def profile_text(self) -> str:
          return (
               f"Steam ID: {code(self.steam_id)}"
               f"\nSteam Name: {bold(self.steam_name)}"
               f"\nTelegram ID: {code(self.telegram_id)}"
               f"\nTelegram username: {bold(self.telegram_username)}"
               f"\nПроцент: {bold(str(self.skin_percent) + '%')}"
          )
     
class SkinSteamInventorySchema(BaseModel):
     name: str
     avatar: str
     
     
class UserPortfolioSkinSchema(BaseModel):
     uuid: str
     user_uuid: str
     skin_name: str
     skin: SkinSchema
     
     
class UserNotifySchema(BaseModel):
     uuid: str
     user_uuid: str
     text: str
     notify_type: str
     created_at: str
     is_read: bool
     user: UserSchema
     