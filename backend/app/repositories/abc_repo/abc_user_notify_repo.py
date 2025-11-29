from typing import Any

from app.schemas.dto import UserNotifyDTO
from ..abc_repository import BaseRepository


class BaseUserNotifyRepository(BaseRepository[UserNotifyDTO, Any]):
     
     async def update_all(self) -> None:
          ...