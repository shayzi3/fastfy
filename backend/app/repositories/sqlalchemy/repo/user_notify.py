from sqlalchemy import update

from app.db.models import UserNotify
from app.schemas.dto import UserNotifyDTO
from ..reposiotry import SQLAlchemyRepository



class SQLAlchemyUserNotifyRepository(SQLAlchemyRepository[UserNotifyDTO, UserNotify]):
     model = UserNotify
     
     async def update_all(
          self,
          data: list[str]
     ) -> None:
          query = (
               update(self.model).
               where(self.model.uuid.in_(data)).
               values(is_read=True).
               execution_options(synchronize_session="fetch")
          )
          await self.session.execute(query)