from typing import Annotated
from fastapi import APIRouter, Depends

from app.responses import isresponse, ArgumentError, NotifyUpdateSuccess
from app.db.session import AsyncSession, get_async_session
from app.infrastracture.redis import RedisPool, get_redis_session
from app.schemas import TokenPayload
from app.api.v1.routers.dependency import current_user

from .service import NotificationService, get_notification_service
from .schema import NotifyID




notification_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User", "User Notification"]
)



@notification_router.get("/notify")
async def get_notify_new(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     service: Annotated[NotificationService, Depends(get_notification_service)],
     current_user: Annotated[TokenPayload, Depends(current_user)]
):
     result = await service.get_notify_new(
          async_session=async_session,
          user_uuid=current_user.uuid
     )
     if isresponse(result):
          return result.response()
     return result
     
     
@notification_router.get("/notify/history")
async def get_notify_history(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     service: Annotated[NotificationService, Depends(get_notification_service)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)]
):
     result = await service.get_notify_history(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid
     )
     if isresponse(result):
          return result.response()
     return result
     
     
@notification_router.patch("/notify")
async def patch_notify(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     service: Annotated[NotificationService, Depends(get_notification_service)],
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     current_user: Annotated[TokenPayload, Depends(current_user)],
     notify_ids: NotifyID
):
     if not notify_ids.ids:
          return ArgumentError.response()
     
     await service.patch_notify(
          async_session=async_session,
          redis_session=redis_session,
          user_uuid=current_user.uuid,
          notify_ids=notify_ids.ids
     )
     return NotifyUpdateSuccess.response()
     
     
     