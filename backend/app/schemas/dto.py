from __future__ import annotations

from datetime import datetime

from typing_extensions import Self
from pydantic import ConfigDict, BaseModel

from app.schemas.enums import NotifyTypeEnum



class PresentationMixin:
     
     def presentation(self, exclude: list[str] = []) -> Self:
          """Метод исключает ненужные поля. Нужен, чтобы не возврщать лишние данные из эндпоинта."""
          
          dump = self.model_dump(exclude=exclude)
          return self.model_construct(**dump)



class UserDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     steam_id: int | None = None
     steam_name: str | None = None
     steam_avatar: str | None = None
     telegram_id: int | None = None
     telegram_username: str | None = None
     created_at: datetime | None = None
     notify: bool | None = None
     
     portfolio_skins: list[SkinPortfolioDTO] = []
     like_skins: list[UserLikeSkinDTO] = []
     notifies: list[UserNotifyDTO] = []
           

               
class SkinDTO(PresentationMixin, BaseModel):
     short_name: str | None = None
     rarity: str | None = None
     color: str | None = None
     category: str | None = None
     weapon: str | None
     
     wears: list[SkinWearDTO] = []
     collections: list[SkinCollectionDTO] = []
     
               
class SkinWearDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     short_name: str | None = None
     market_hash_name: str | None = None
     image_link: str | None = None
     wear: str | None
     phase: str | None
     stattrak: bool | None
     souvenir: bool | None
     price: float | None = None
     price_last_1_day: float | None = None
     price_last_7_day: float | None = None
     price_last_30_day: float | None = None
     price_last_365_day: float | None = None
     price_last_all_day: float | None = None
     last_price: float | None = None
     last_price_update: datetime | None = None
     sell_by_last_update: int | None = None
     
     skin: SkinDTO | None = None
     price_history: list[SkinPriceHistoryDTO] = []
     portfolio_skins: list[SkinPortfolioDTO] = []
     transaction_skins: list[SkinPortfolioTransactionDTO] = []
     like_skins: list[UserLikeSkinDTO] = []
     
     
     
class SkinPriceHistoryDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     skin_wear_uuid: str | None = None
     volume: int | None = None
     price: float | None = None
     timestamp: datetime | None = None
     
     skin_wear: SkinWearDTO | None = None
     
               
     
class SkinPortfolioDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     user_uuid: str | None = None
     skin_wear_uuid: str | None = None
     benefit: float | None = None
     notify_percent: int | None = None
     
     skin_wear: SkinWearDTO | None = None
     user: UserDTO | None = None
     transations: list[SkinPortfolioTransactionDTO] = []
     
     
               
               
class SkinPortfolioTransactionDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     portfolio_skin_uuid: str | None = None
     skin_wear_uuid: str | None = None
     comment: str | None = None
     count: int | None = None
     buy_price: float | None = None
     when_buy: datetime | None = None
     
     skin_wear: SkinWearDTO | None = None
     skin_portfolio: SkinPortfolioDTO | None = None
     
     
class UserLikeSkinDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     user_uuid: str | None = None
     skin_wear_uuid: str | None = None
     short_name: str | None = None
     
     user: UserDTO | None = None
     skin: SkinDTO | None = None
     skin_wear: SkinWearDTO | None = None
     
     
class UserNotifyDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     user_uuid: str | None = None
     text: str | None = None
     notify_type: NotifyTypeEnum | None = None
     created_at: datetime | None = None
     is_read: bool | None = None
     
     user: UserDTO | None = None
     
     model_config = ConfigDict(use_enum_values=True)
               
      
class SkinCollectionDTO(PresentationMixin, BaseModel):
     uuid: str | None = None
     short_name: str | None = None
     collection: str | None = None
     image_link: str | None = None
     is_collection: bool | None = None
     is_rare: bool | None = None
     
     skin: SkinDTO | None = None