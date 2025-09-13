from app.responses.abstract import AbstractResponse
from app.responses import NotifyEmpty
from app.schemas import UserNotifyModel
from app.schemas.enums import NotifyType
from app.db.repository import UserNotifyRepository
from app.db.session import AsyncSession



class NotificationService:
     def __init__(self):
          self.notify_repository = UserNotifyRepository
          
          
     async def get_notify_new(
          self,
          async_session: AsyncSession,
     ) -> list[UserNotifyModel] | AbstractResponse:
          result = await self.notify_repository.read_all(
               session=async_session,
               selectload=True,
               is_read=False,
               notify_type=NotifyType.SKIN
          )
          if not result:
               return NotifyEmpty
          return result
     
     async def patch_notify(
          self,
          async_session: AsyncSession,
          notifies: list[UserNotifyModel]
     ) -> None:
          update_notify = [nt.uuid for nt in notifies]
          await self.notify_repository.update_all(
               session=async_session,
               data=update_notify
          )
          
          
          
async def get_notification_service() -> NotificationService:
     return NotificationService()