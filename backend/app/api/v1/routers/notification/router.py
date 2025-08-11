from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks

from app.responses import (
     isresponse, 
     router_responses,
     NotifyEmpty,
     AuthError,
     ServerError,
     SecretTokenError
)
from app.db.session import AsyncSession, get_async_session
from app.schemas import UserNotifyModel
from app.api.v1.routers.dependency import valide_secret_bot_token

from .service import NotificationService, get_notification_service


notification_router = APIRouter(
     prefix="/api/v1/user",
     tags=["User", "User Notification", "Bot"],
     dependencies=[Depends(valide_secret_bot_token)],
)



@notification_router.get(
     path="/notify", 
     response_model=list[UserNotifyModel],
     responses=router_responses(
          NotifyEmpty,
          AuthError,
          ServerError,
          SecretTokenError
     )
)
async def get_notify_new(
     async_session: Annotated[AsyncSession, Depends(get_async_session)],
     service: Annotated[NotificationService, Depends(get_notification_service)],
     background_task: BackgroundTasks
):
     result = await service.get_notify_new(async_session=async_session)
     if isresponse(result):
          return result.response()
     
     background_task.add_task(
          func=service.patch_notify,
          async_session=async_session,
          notifies=result
     )
     return result
     
     