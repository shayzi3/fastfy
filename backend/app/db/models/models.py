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
     SkinRelModel
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
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, unique=True, default=uuid.uuid4())
     steam_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
     steam_name: Mapped[str] = mapped_column(nullable=False)
     steam_avatar: Mapped[str] = mapped_column(nullable=False)
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
     __table_args__ = (
          Index("idx_skin_name", "name"),
     )
     pydantic_model = SkinModel
     pydantic_rel_model = SkinRelModel
     
     id: Mapped[str] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(nullable=False)
     avatar: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[float] = mapped_column(nullable=False)
     price_last_1_day: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_30_day: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_365_day: Mapped[float] = mapped_column(nullable=True) # percent
     
     history: Mapped[list["SkinsPriceHistory"]] = relationship(
          uselist=True,
          cascade="all, delete-orphan"
     )
     
     @classmethod
     def selectinload(cls):
          return cls.history
     
     @classmethod
     def returning(cls):
          return cls.id
     
     
     
class SkinsPriceHistory(Base):
     __tablename__ = "skins_price_history"
     __table_args__ = (
          Index("idx_skin_history_name", "skin_name"),
          Index("idx_skin_history_id", "skin_id"),
          Index("idx_skin_history_timestamp", "timestamp")
     )
     pydantic_model = SkinPriceHistoryModel
     
     item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     skin_id: Mapped[str] = mapped_column(ForeignKey("skins.id", ondelete="CASCADE"))
     skin_name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[float] = mapped_column(nullable=False)
     volume: Mapped[int] = mapped_column(nullable=False)
     timestamp: Mapped[datetime] = mapped_column(nullable=False)
     
     
     
class UsersPortfolio(Base):
     __tablename__ = "users_portfolio"
     __table_args__ = (
          Index("idx_portfolio_user_uuid", "user_uuid"),
          Index("idx_portfolio_skin_id", "skin_id")
     )
     pydantic_model = UserPortfolioModel
     
     item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     user_uuid: Mapped[str] = mapped_column(UUID(), ForeignKey("users.uuid", ondelete="CASCADE"))
     skin_id: Mapped[str] = mapped_column(ForeignKey("skins.id"))
     quantity: Mapped[int] = mapped_column(default=1, nullable=False)
     buy_price: Mapped[float] = mapped_column(nullable=False)
     