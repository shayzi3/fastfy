from datetime import datetime
from sqlalchemy import BigInteger, Index, ForeignKey, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.enums import UpdateMode, NotifyType

from .base import Base
from .mixins import (
     UsersMixin,
     SkinsMixin,
     SkinsPriceInfoMixin,
     SkinsPriceHistoryMixin,
     UsersNotifyMixin,
     UsersSkinsMixin
)



class Users(UsersMixin, Base):
     __tablename__ = "users"
     __table_args__ = (
          Index("idx_steam_id", "steam_id"),
          Index("idx_telegram_id", "telegram_id")
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     steam_id: Mapped[int] = mapped_column(BigInteger)
     steam_name: Mapped[str] = mapped_column()
     steam_avatar: Mapped[str] = mapped_column()
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     skin_percent: Mapped[int] = mapped_column(default=10)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Skins(SkinsMixin, Base):
     __tablename__ = "skins"
     
     name: Mapped[str] = mapped_column(primary_key=True)
     image: Mapped[str] = mapped_column()
     
     skin_price_info: Mapped["SkinsPriceInfo"] = relationship(
          cascade="all, delete-orphan",
          lazy="joined"
     )
 

class SkinsPriceInfo(SkinsPriceInfoMixin, Base):
     __tablename__ = "skins_price_info"
     __table_args__ = (
          Index("idx_skin_name", "skin_name"),
          Index("idx_update_mode", "update_mode"),
     )
     
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"), primary_key=True)
     update_mode: Mapped[UpdateMode] = mapped_column(default=UpdateMode.HIGH)
     last_update: Mapped[datetime] = mapped_column(nullable=True)
     price: Mapped[float] = mapped_column(nullable=True)
     price_last_1_day: Mapped[float] = mapped_column(nullable=True)
     price_last_30_day: Mapped[float] = mapped_column(nullable=True)
     price_last_365_day: Mapped[float] = mapped_column(nullable=True)
     
     
     
class SkinsPriceHistory(SkinsPriceHistoryMixin, Base):
     __tablename__ = "skins_price_history"
     __table_args__ = (
          Index("idx_skin_history_name", "skin_name"),
          Index("idx_skin_history_timestamp", "timestamp")
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     price: Mapped[float] = mapped_column()
     volume: Mapped[int] = mapped_column()
     timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
     
          

class UsersSkins(UsersSkinsMixin, Base):
     __tablename__ = "users_skins"
     __table_args__ = (
          Index("idx_portfolio_user_uuid", "user_uuid"),
          Index("idx_portfolio_skin_name", "skin_name")
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     user_uuid: Mapped[str] = mapped_column(UUID(), ForeignKey("users.uuid", ondelete="CASCADE"))
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     
     skin: Mapped["Skins"] = relationship()
     user: Mapped["Users"] = relationship()
     
     
     
class UsersNotify(UsersNotifyMixin, Base):
     __tablename__ = "users_notify"
     __table_args__ = (
          Index("idx_notify_user_uuid", "user_uuid"),
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     user_uuid: Mapped[str] = mapped_column(UUID(), ForeignKey("users.uuid", ondelete="CASCADE"))
     text: Mapped[str] = mapped_column()
     notify_type: Mapped[NotifyType] = mapped_column()
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     is_read: Mapped[bool] = mapped_column(default=False)
     
     user: Mapped["Users"] = relationship()