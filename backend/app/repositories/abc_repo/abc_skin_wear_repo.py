from typing import Any

from app.schemas.dto import SkinWearDTO
from ..abc_repository import BaseRepository



class BaseSkinWearRepository(BaseRepository[SkinWearDTO, Any]):
     ...