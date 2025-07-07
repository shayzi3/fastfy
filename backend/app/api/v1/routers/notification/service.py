from app.responses.abstract import AbstractResponse
from app.responses import NotifyEmpty, NotifyUpdateSuccess
from app.schemas import UserNotifyModel
from app.db.repository import NotifyRepository
from app.db.session import AsyncSession
from app.infrastracture.redis import RedisPool



class NotificationService:
     def __init__(self):
          self.notify_repository = NotifyRepository
          
          
     async def get_notify_new(
          self,
          async_session: AsyncSession,
          user_uuid: str
     ) -> list[UserNotifyModel] | AbstractResponse:
          result = await self.notify_repository.read_all(
               session=async_session,
               user_uuid=user_uuid,
               is_read=False
          )
          if not result:
               return NotifyEmpty
          return result
     
     
     async def get_notify_history(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str
     ) -> list[UserNotifyModel] | AbstractResponse:
          result = await self.notify_repository.read_all(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"notify_history:{user_uuid}",
               user_uuid=user_uuid
          )
          if not result:
               return NotifyEmpty
          return result
     
     
     async def patch_notify(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          notify_ids: list[str]
     ) -> None:
          await self.notify_repository.update_all(
               session=async_session,
               redis_session=redis_session,
               notify_ids=notify_ids,
               delete_redis_values=[f"notify_history:{user_uuid}"]
          )
          
          
          
async def get_notification_service() -> NotificationService:
     return NotificationService()