import uuid

from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, func, Enum, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import (
     UserMixin,
     SkinMixin,
     SkinPriceHistoryMixin,
     UserNotifyMixin,
     SkinPortfolioMixin,
     SkinPortfolioTransactionMixin,
     UserLikeSkinMixin,
     SkinCollectionMixin,
     SkinWearMixin
)



class User(UserMixin, Base):
     __tablename__ = "users"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     steam_id: Mapped[int] = mapped_column(BigInteger, index=True)
     steam_name: Mapped[str] = mapped_column()
     steam_avatar: Mapped[str] = mapped_column()
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True, index=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     notify: Mapped[bool] = mapped_column(default=True)
     
     portfolio_skins: Mapped[list["SkinPortfolio"]] = relationship(back_populates="user")
     like_skins: Mapped[list["UserLikeSkin"]] = relationship(back_populates="user")
     notifies: Mapped[list["UserNotify"]] = relationship(back_populates="user")
     
class Skin(SkinMixin, Base):
     __tablename__ = "skins"
     
     short_name: Mapped[str] = mapped_column(primary_key=True)
     category: Mapped[str] = mapped_column(index=True)
     weapon: Mapped[str] = mapped_column(index=True, nullable=True)
     rarity: Mapped[str] = mapped_column(index=True)
     color: Mapped[str] = mapped_column()
     
     wears: Mapped[list["SkinWear"]] = relationship(back_populates="skin")
     collections: Mapped[list["SkinCollection"]] = relationship(back_populates="skin")
     like_skins: Mapped[list["UserLikeSkin"]] = relationship(back_populates="skin")


class SkinWear(SkinWearMixin, Base):
     __tablename__ = "skins_wears"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     short_name: Mapped[str] = mapped_column(ForeignKey("skins.short_name", ondelete="CASCADE", onupdate="CASCADE"))
     market_hash_name: Mapped[str] = mapped_column()
     image_link: Mapped[str] = mapped_column()
     wear: Mapped[str] = mapped_column(index=True, nullable=True)
     phase: Mapped[str] = mapped_column(nullable=True)
     stattrak: Mapped[bool] = mapped_column(nullable=True)
     souvenir: Mapped[bool] = mapped_column(nullable=True)
     price: Mapped[float] = mapped_column(nullable=True)
     price_last_1_day: Mapped[float] = mapped_column(nullable=True)
     price_last_7_day: Mapped[float] = mapped_column(nullable=True)
     price_last_30_day: Mapped[float] = mapped_column(nullable=True)
     price_last_365_day: Mapped[float] = mapped_column(nullable=True)
     price_last_all_day: Mapped[float] = mapped_column(nullable=True)
     last_price: Mapped[float] = mapped_column(nullable=True)
     last_price_update: Mapped[datetime] = mapped_column(nullable=True)
     sell_by_last_update: Mapped[int] = mapped_column(nullable=True)
     
     skin: Mapped["Skin"] = relationship(back_populates="wears")
     price_history: Mapped[list["SkinPriceHistory"]] = relationship(back_populates="skin_wear")
     portfolio_skins: Mapped[list["SkinPortfolio"]] = relationship(back_populates="skin_wear")
     transaction_skins: Mapped[list["SkinPortfolioTransaction"]] = relationship(back_populates="skin_wear")
     like_skins: Mapped[list["UserLikeSkin"]] = relationship(back_populates="skin_wear")
     
     
class SkinPriceHistory(SkinPriceHistoryMixin, Base):
     __tablename__ = "skins_price_history"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     skin_wear_uuid: Mapped[str] = mapped_column(
          ForeignKey("skins_wears.uuid", ondelete="CASCADE", onupdate="CASCADE"),
          index=True
     )
     volume: Mapped[int] = mapped_column()
     price: Mapped[float] = mapped_column()
     timestamp: Mapped[datetime] = mapped_column(index=True)
     
     skin_wear: Mapped["SkinWear"] = relationship(back_populates="price_history")
          

class SkinPortfolio(SkinPortfolioMixin, Base):
     __tablename__ = "skins_portfolio"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     user_uuid: Mapped[str] = mapped_column(
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     skin_wear_uuid: Mapped[str] = mapped_column(
          ForeignKey("skins_wears.uuid", ondelete="CASCADE", onupdate="CASCADE")
     )
     benefit: Mapped[float] = mapped_column(default=0)
     notify_percent: Mapped[int] = mapped_column(default=10)
     
     skin_wear: Mapped["SkinWear"] = relationship(back_populates="portfolio_skins")
     user: Mapped["User"] = relationship(back_populates="portfolio_skins")
     transactions: Mapped[list["SkinPortfolioTransaction"]] = relationship(back_populates="skin_portfolio")


     
class SkinPortfolioTransaction(SkinPortfolioTransactionMixin, Base):
     __tablename__ = "skins_portfolio_transactions"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     portfolio_skin_uuid: Mapped[str] = mapped_column(
          ForeignKey("skins_portfolio.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     skin_wear_uuid: Mapped[str] = mapped_column(
          ForeignKey("skins_wears.uuid", onupdate="CASCADE", ondelete="CASCADE"),
     )
     comment: Mapped[str] = mapped_column(nullable=True)
     count: Mapped[int] = mapped_column()
     buy_price: Mapped[float] = mapped_column()
     when_buy: Mapped[datetime] = mapped_column(nullable=True)
     
     skin_wear: Mapped["SkinWear"] = relationship(back_populates="transaction_skins")
     skin_portfolio: Mapped["SkinPortfolio"] = relationship(back_populates="transactions")
     
     
     
class UserLikeSkin(UserLikeSkinMixin, Base):
     __tablename__ = "users_likes_skins"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     user_uuid: Mapped[str] = mapped_column( 
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     skin_wear_uuid: Mapped[str] = mapped_column(
          ForeignKey("skins_wears.uuid", onupdate="CASCADE", ondelete="CASCADE"),
     )
     short_name: Mapped[str] = mapped_column(
          ForeignKey("skins.short_name", onupdate="CASCADE", ondelete="CASCADE"),
     )
     
     user: Mapped["User"] = relationship(back_populates="like_skins")
     skin_wear: Mapped["SkinWear"] = relationship(back_populates="like_skins")
     skin: Mapped["Skin"] = relationship(back_populates="like_skins")
     
     
     
class UserNotify(UserNotifyMixin, Base):
     __tablename__ = "users_notifies"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     user_uuid: Mapped[str] = mapped_column(
          ForeignKey("users.uuid", ondelete="CASCADE", onupdate="CASCADE"), 
          index=True
     )
     text: Mapped[str] = mapped_column()
     notify_type: Mapped[str] = mapped_column(Enum("INFO", "SKIN", name="notify_type_enum"), index=True)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     is_read: Mapped[bool] = mapped_column(default=False)
     
     user: Mapped["User"] = relationship(back_populates="notifies")
     
      
      
class SkinCollection(SkinCollectionMixin, Base):
     __tablename__ = "skins_collections"
     
     uuid: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
     short_name: Mapped[str] = mapped_column(
          ForeignKey("skins.short_name", ondelete="CASCADE", onupdate="CASCADE"),
          index=True
     )
     collection: Mapped[str] = mapped_column(index=True)
     image_link: Mapped[str] = mapped_column()
     is_collection: Mapped[bool] = mapped_column()
     is_rare: Mapped[bool] = mapped_column()
     
     skin: Mapped["Skin"] = relationship(back_populates="collections")