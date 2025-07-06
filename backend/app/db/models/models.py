import uuid

from datetime import datetime
from sqlalchemy import BigInteger, Index, func, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.schemas import (
     SkinModel,
     UserModel,
     UserRelModel,
     SkinPriceHistoryModel,
     UserPortfolioModel,
     UserPortfolioRelModel
)
from .base import Base




class Users(Base):
     __tablename__ = "users"
     __table_args__ = (
          Index("idx_steam_id", "steam_id"),
          Index("idx_telegram_id", "telegram_id")
     )
     pydantic_model = UserModel
     pydantic_rel_model = UserRelModel
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4())
     steam_id: Mapped[int] = mapped_column(BigInteger)
     steam_name: Mapped[str] = mapped_column()
     steam_avatar: Mapped[str] = mapped_column()
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(default=func.now())
     
     portfolio: Mapped[list["UsersPortfolio"]] = relationship(
          uselist=True,
          cascade="all, delete-orphan"
     )
     
     @classmethod
     def selectinload(cls):
          return cls.portfolio
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     
  
class Skins(Base):
     __tablename__ = "skins"
     pydantic_model = SkinModel
     
     name: Mapped[str] = mapped_column(primary_key=True)
     avatar: Mapped[str] = mapped_column()
     price: Mapped[float] = mapped_column()
     price_last_1_day: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_30_day: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_365_day: Mapped[float] = mapped_column(nullable=True) # percent
     
     @classmethod
     def returning(cls):
          return cls.name
     
     
     
class SkinsPriceHistory(Base):
     __tablename__ = "skins_price_history"
     __table_args__ = (
          Index("idx_skin_history_name", "skin_name"),
          Index("idx_skin_history_timestamp", "timestamp")
     )
     pydantic_model = SkinPriceHistoryModel
     
     item_id: Mapped[str] = mapped_column(UUID(), primary_key=True)
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     price: Mapped[float] = mapped_column(nullable=False)
     volume: Mapped[int] = mapped_column(nullable=False)
     timestamp: Mapped[datetime] = mapped_column(nullable=False)
     
     
     @classmethod
     def returning(cls):
          return cls.item_id
     
     

class UsersPortfolio(Base):
     __tablename__ = "users_portfolio"
     __table_args__ = (
          Index("idx_portfolio_user_uuid", "user_uuid"),
          Index("idx_portfolio_skin_name", "skin_name")
     )
     pydantic_model = UserPortfolioModel
     pydantic_rel_model = UserPortfolioRelModel
     
     item_id: Mapped[str] = mapped_column(UUID(), primary_key=True)
     user_uuid: Mapped[str] = mapped_column(UUID(), ForeignKey("users.uuid", ondelete="CASCADE"))
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     quantity: Mapped[int] = mapped_column(default=1, nullable=False)
     buy_price: Mapped[float] = mapped_column(nullable=False)
     
     skin: Mapped["Skins"] = relationship()
     
     @classmethod 
     def selectinload(cls):
          return cls.skin
     
     @classmethod
     def returning(cls):
          return cls.item_id
     