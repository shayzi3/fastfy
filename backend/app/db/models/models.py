from datetime import datetime
from sqlalchemy import BigInteger, Index, func, Table, Column, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas import (
     SkinModel,
     SkinRelModel,
     UserModel,
     UserRelModel,
     SkinPriceHistoryModel
)
from .base import Base


 

assotiation_table = Table(
     "assotiation",
     Base.metadata,
     Column("uuid", ForeignKey("users.uuid"), primary_key=True, unique=True),
     Column("id", ForeignKey("skins.skin_id"), primary_key=True, unique=True)
)



class Users(Base):
     __tablename__ = "users"
     __table_args__ = (
          Index("idx_steam_id", "steam_id"),
          Index("idx_telegram_id", "telegram_id")
     )
     pydantic_model = UserModel
     pydantic_rel_model = UserRelModel
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, unique=True)
     steam_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
     steam_name: Mapped[str] = mapped_column(nullable=False)
     steam_avatar: Mapped[str] = mapped_column(nullable=False)
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(default=func.now())
     
     skins: Mapped[list["Skins"]] = relationship(
          "Skins",
          secondary=assotiation_table,
          back_populates="users",
          uselist=True
     )
     
     @classmethod
     def selectinload(cls):
          return cls.skins
     
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     
  
class Skins(Base):
     __tablename__ = "skins"
     __table_args__ = (
          Index("idx_skin_name", "skin_name"),
          Index("idx_rarity", "rarity"),
          Index("idx_collection", "collection"),
          Index("idx_item_type", "item_type")
     )
     pydantic_model = SkinModel
     pydantic_rel_model = SkinRelModel
     
     skin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     skin_name: Mapped[str] = mapped_column(nullable=False)
     skin_avatar: Mapped[str] = mapped_column(nullable=False)
     skin_price: Mapped[float] = mapped_column(nullable=False)
     rarity: Mapped[str] = mapped_column(nullable=False)
     collection: Mapped[str] = mapped_column(nullable=False)
     item_type: Mapped[str] = mapped_column(nullable=False)
     price_last_1_day: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_7_days: Mapped[float] = mapped_column(nullable=True) # percent
     price_last_30_days: Mapped[float] = mapped_column(nullable=True) # percent
     
     users: Mapped[list["Users"]] = relationship(
          "Users",
          secondary=assotiation_table,
          back_populates="skins",
          uselist=True
     )
     
     @classmethod
     def selectinload(cls):
          return cls.users
     
     @classmethod
     def returning(cls):
          return cls.skin_id
     
     
     
class SkinsPriceHistory(Base):
     __tablename__ = "skins_price_history"
     __table_args__ = (
          Index("idx_skin_history_name", "skin_name"),
          Index("idx_skin_history_timestamp", "timestamp")
     )
     pydantic_model = SkinPriceHistoryModel
     
     skin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     skin_name: Mapped[str] = mapped_column(nullable=False)
     price: Mapped[float] = mapped_column(nullable=False)
     timestamp: Mapped[datetime] = mapped_column(default=func.now())