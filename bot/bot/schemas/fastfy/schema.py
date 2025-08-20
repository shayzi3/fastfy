from typing import Any, TypeVar, Generic
from pydantic import BaseModel



SKINS_ON_PAGE = TypeVar("SKINS_ON_PAGE", bound=BaseModel)



class ResponseObjectSchema(BaseModel):
     status_code: int
     obj: dict[str, Any] | list[dict[str, Any]]


class DetailSchema(BaseModel):
     is_detail: bool = True
     detail: str
     
     
class _SkinPriceInfoSchema(BaseModel):
     skin_name: str
     update_mode: int
     last_update: str
     price: float
     price_at_1_day: float
     price_at_30_day: float
     price_at_365_day: float
     

     
class SkinSchema(BaseModel):
     name: str
     image: str
     skin_price_info: _SkinPriceInfoSchema | None
     

     
class SkinsOnPageSchema(BaseModel, Generic[SKINS_ON_PAGE]):
     pages: int
     current_page: int
     skins: list[SKINS_ON_PAGE]
     skin_model: SKINS_ON_PAGE
     
     def model_post_init(self, _: Any):
          self.skins = [
               self.skin_model.model_validate(json_model)
               for json_model in self.skins
          ]
          
          
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
     notify_type: int
     created_at: str
     is_read: bool
     user: UserSchema
     