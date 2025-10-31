from typing import Any

from app.schemas.dto import PortfolioSkinTransactionDTO
from ..abc_repository import BaseRepository




class BasePortfolioSkinTransactionRepository(BaseRepository[PortfolioSkinTransactionDTO, Any]):
     ...