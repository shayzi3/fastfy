import uuid

from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import func, UUID, BigInteger

from app.schemas import UserModel
from app.db.models import Base




class Users(Base):
     __tablename__ = "users"
     pydantic_model = UserModel
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True, unique=True)
     steam_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
     steam_name: Mapped[str] = mapped_column(nullable=False)
     steam_avatar: Mapped[str] = mapped_column(nullable=False)
     telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
     telegram_username: Mapped[str] = mapped_column(nullable=True)
     created_at: Mapped[datetime] = mapped_column(default=func.now())