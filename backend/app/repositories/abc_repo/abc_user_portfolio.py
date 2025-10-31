from typing import Any

from app.infrastracture.cache.abc import Cache
from app.schemas.dto import UserPortfolioDTO
from app.schemas import SkinsPage
from ..abc_repository import BaseRepository


class BaseUserPortfolioRepository(BaseRepository[UserPortfolioDTO, Any]):
     ...