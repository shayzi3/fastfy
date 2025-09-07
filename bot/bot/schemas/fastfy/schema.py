from typing import Any, TypeVar, Generic, Type
from pydantic import BaseModel, model_validator

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
     

     
class SkinsOnPageSchema(BaseModel, Generic[SKINS_ON_PAGE]):
     pages: int
     current_page: int
     skins: list[SKINS_ON_PAGE]
     skin_model: Type[BaseModel]
     
     @model_validator(mode="before")
     def validator(data: dict[str, Any]) -> dict[str, Any]:
          skin_model: Type[BaseModel] = data["skin_model"]
          data["skins"] = [
               skin_model.model_validate(skin_data)
               for skin_data in data["skins"]
          ]
          return data
          
          
class _HistortSchema(BaseModel):
     price: float
     volume: int
     timestamp: str
     
       
class SkinPriceHistorySchema(BaseModel):
     all: list[_HistortSchema]
     year: list[_HistortSchema]
     month: list[_HistortSchema]
     day: list[_HistortSchema]
     
     
     
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
               f"Steam ID: {self.steam_id}"
               f"\nSteam Name: {self.steam_name}"
               f"\nTelegram ID: {self.telegram_id}"
               f"\nTelegram username: {self.telegram_username}"
               f"\nПроцент: {self.skin_percent}"
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
     