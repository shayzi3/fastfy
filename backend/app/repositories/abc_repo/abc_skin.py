from typing import Any

from app.schemas.dto import SkinDTO
from app.schemas import SkinsPage
from ..abc_repository import BaseRepository



class BaseSkinRepository(BaseRepository[SkinDTO, Any]):
     ...