from typing import Any

from app.schemas.dto import SkinPortfolioTransactionDTO
from ..abc_repository import BaseRepository




class BaseSkinPortfolioTransactionRepository(BaseRepository[SkinPortfolioTransactionDTO, Any]):
     ...