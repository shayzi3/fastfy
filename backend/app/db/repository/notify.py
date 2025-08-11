from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.schemas import UserNotifyModel
from app.db.models.models import UsersNotify
from .base import BaseRepository



class UserNotifyRepository(BaseRepository[UserNotifyModel, None]):
     model = UsersNotify
     
     
     @classmethod
     async def update_all(
          cls,
          session: AsyncSession,
          data: list[str]
     ) -> None:
          sttm = (
               update(UsersNotify).
               where(UsersNotify.uuid.in_(data)).
               values(is_read=True).
               execution_options(synchronize_session="fetch")
          )
          await session.execute(sttm)
          await session.commit()
