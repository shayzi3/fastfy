from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict
from typing_extensions import Literal

from app.schemas.presentation import BaseModelPresentation
from app.schemas.presentation.dto import (
     SkinDTOPresentation,
     SkinCollectionDTOPresentation,
     SkinPriceHistoryDTOPresentation,
     UserLikeSkinDTOPresentation,
     PortfolioSkinTransactionDTOPresentation,
     UserPortfolioDTOPresentation,
     UserNotifyDTOPresentation
)





class UserDTO(BaseModelPresentation):
     uuid: UUID
     steam_id: int
     steam_name: str
     steam_avatar: str
     telegram_id: int | None = None
     telegram_username: str | None = None
     created_at: datetime
     notify: bool  
           

               
class SkinDTO(BaseModelPresentation[SkinDTOPresentation]):
     _presentation = SkinDTOPresentation
     
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
     
     model_config = ConfigDict(arbitrary_types_allowed=True)
               
     
     
class SkinPriceHistoryDTO(BaseModelPresentation[SkinPriceHistoryDTOPresentation]):
     _presentation = SkinPriceHistoryDTOPresentation
     
     uuid: UUID
     market_hash_name: str
     volume: int
     price: float
     timestamp: datetime
     
               
     
class UserPortfolioDTO(BaseModelPresentation[UserPortfolioDTOPresentation]):
     _presentation = UserPortfolioDTOPresentation
     
     uuid: UUID
     user_uuid: str
     market_hash_name: str
     benefit: float
     notify_percent: int
     
     skin: SkinDTO
     user: UserDTO | None = None
     transations: list["PortfolioSkinTransactionDTO"] = []
     
     model_config = ConfigDict(arbitrary_types_allowed=True)
     
               
               
class PortfolioSkinTransactionDTO(BaseModelPresentation[PortfolioSkinTransactionDTOPresentation]):
     _presentation = PortfolioSkinTransactionDTOPresentation
     
     uuid: UUID
     portfolio_skin_uuid: str
     comment: str
     count: int
     buy_price: float
     when_buy: datetime | None = None
     
     
class UserLikeSkinDTO(BaseModelPresentation[UserLikeSkinDTOPresentation]):
     _presentation = UserLikeSkinDTOPresentation
     
     uuid: UUID
     user_uuid: str
     market_hash_name: str
     short_name: str
     skin: SkinDTO
     
     
class UserNotifyDTO(BaseModelPresentation[UserNotifyDTOPresentation]):
     _presentation = UserNotifyDTOPresentation
     
     uuid: UUID
     user_uuid: str
     text: str
     notify_type: Literal["SKIN", "INFO"]
     created_at: datetime
     is_read: bool
     user: UserDTO
               
               
class SkinCollectionDTO(BaseModelPresentation[SkinCollectionDTOPresentation]):
     _presentation = SkinCollectionDTOPresentation
     
     uuid: UUID
     market_hash_name: str
     short_name: str
     collection: str
     image_link: str
     is_collection: bool
     is_rare: bool