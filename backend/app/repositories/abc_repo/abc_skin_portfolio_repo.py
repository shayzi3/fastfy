from typing import Any

from app.schemas.dto import SkinPortfolioDTO
from ..abc_repository import BaseRepository


class BaseSkinPortfolioRepository(BaseRepository[SkinPortfolioDTO, Any]):
     ...