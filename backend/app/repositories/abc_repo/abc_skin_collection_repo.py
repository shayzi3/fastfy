from typing import Any

from app.schemas.dto import SkinCollectionDTO
from ..abc_repository import BaseRepository




class BaseSkinCollectionRepository(BaseRepository[SkinCollectionDTO, Any]):
     ...