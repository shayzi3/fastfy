import uuid

from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import (
     UserMixin,
     SkinMixin,
     SkinPriceHistoryMixin,
     UserNotifyMixin,
     UserPortfolioMixin,
     PortfolioSkinTransactionMixin,
     UserLikeSkinMixin,
     SkinCollectionMixin
)



class User(UserMixin, Base):
     __tablename__ = "users"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     steam_id: Mapped[int] = mapped_column(BigInteger, index=True)
     steam_name: Mapped[str] = mapped_column()
     steam_avatar: Mapped[str] = mapped_column()
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True, index=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     notify: Mapped[bool] = mapped_column(default=True)


class Skin(SkinMixin, Base):
     __tablename__ = "skins"

     market_hash_name: Mapped[str] = mapped_column(primary_key=True)
     short_name: Mapped[str] = mapped_column(index=True)
     category: Mapped[str] = mapped_column(index=True)
     weapon: Mapped[str] = mapped_column(index=True, nullable=True)
     wear: Mapped[str] = mapped_column(index=True, nullable=True)
     rarity: Mapped[str] = mapped_column(index=True)
     color: Mapped[str] = mapped_column()
     stattrak: Mapped[bool] = mapped_column(default=False, nullable=True)
     souvenir: Mapped[bool] = mapped_column(default=False, nullable=True)
     image_link: Mapped[str] = mapped_column()
     price: Mapped[float] = mapped_column(nullable=True)
     price_last_1_day: Mapped[float] = mapped_column(nullable=True)
     price_last_7_day: Mapped[float] = mapped_column(nullable=True)
     price_last_30_day: Mapped[float] = mapped_column(nullable=True)
     price_last_365_day: Mapped[float] = mapped_column(nullable=True)
     price_last_all_day: Mapped[float] = mapped_column(nullable=True)
     last_price: Mapped[float] = mapped_column(nullable=True)
     last_price_update: Mapped[datetime] = mapped_column(nullable=True)
     sell_by_last_update: Mapped[int] = mapped_column(default=0)
     
     collections: Mapped[list["SkinCollection"]] = relationship()

     
class SkinPriceHistory(SkinPriceHistoryMixin, Base):
     __tablename__ = "skins_price_history"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     market_hash_name: Mapped[str] = mapped_column(
          ForeignKey("skins.market_hash_name", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     volume: Mapped[int] = mapped_column()
     price: Mapped[float] = mapped_column()
     timestamp: Mapped[datetime] = mapped_column(index=True)
     
          

class UserPortfolio(UserPortfolioMixin, Base):
     __tablename__ = "users_portfolio"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     user_uuid: Mapped[str] = mapped_column(UUID(), 
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     market_hash_name: Mapped[str] = mapped_column(
          ForeignKey("skins.market_hash_name", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     benefit: Mapped[float] = mapped_column(default=0)
     notify_percent: Mapped[int] = mapped_column(default=10)
     
     skin: Mapped["Skin"] = relationship()
     user: Mapped["User"] = relationship()
     transactions: Mapped[list["PortfolioSkinTransaction"]] = relationship(uselist=True)

     
class PortfolioSkinTransaction(PortfolioSkinTransactionMixin, Base):
     __tablename__ = "portfolio_skins_transactions"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     portfolio_skin_uuid: Mapped[str] = mapped_column(UUID(), 
          ForeignKey("users_portfolio.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     comment: Mapped[str] = mapped_column()
     count: Mapped[int] = mapped_column()
     buy_price: Mapped[float] = mapped_column()
     when_buy: Mapped[datetime] = mapped_column(nullable=True)
     
     
     
class UserLikeSkin(UserLikeSkinMixin, Base):
     __tablename__ = "users_likes_skins"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     user_uuid: Mapped[str] = mapped_column(UUID(), 
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     market_hash_name: Mapped[str] = mapped_column(
          ForeignKey("skins.market_hash_name", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     skin: Mapped["Skin"] = relationship()     
     
     
class UserNotify(UserNotifyMixin, Base):
     __tablename__ = "users_notifies"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4()) 
     text: Mapped[str] = mapped_column()
     notify_type: Mapped[str] = mapped_column(index=True)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)
     is_read: Mapped[bool] = mapped_column(default=False)
     user_uuid: Mapped[str] = mapped_column(UUID(), 
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     user: Mapped["User"] = relationship()
     
      
     
class SkinCollection(SkinCollectionMixin, Base):
     __tablename__ = "skins_collections"
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
     market_hash_name: Mapped[str] = mapped_column(
          ForeignKey("skins.market_hash_name", ondelete="CASCADE", onupdate="CASCADE"),
          index=True
     )
     short_name: Mapped[str] = mapped_column()
     collection: Mapped[str] = mapped_column(index=True)
     image_link: Mapped[str] = mapped_column()
     is_collection: Mapped[bool] = mapped_column()
     is_rare: Mapped[bool] = mapped_column()