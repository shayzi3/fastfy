from typing import Any

from app.schemas.dto import UserLikeSkinDTO
from ..abc_repository import BaseRepository




class BaseUserLikeSkinRepository(BaseRepository[UserLikeSkinDTO, Any]):
     ...