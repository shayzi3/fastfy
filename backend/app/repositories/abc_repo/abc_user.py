from typing import Any

from app.schemas.dto import UserDTO
from ..abc_repository import BaseRepository




class BaseUserRepository(BaseRepository[UserDTO, Any]):
     ...