from app.db.models import PortfolioSkinTransaction
from app.schemas.dto import PortfolioSkinTransactionDTO
from ..reposiotry import SQLAlchemyRepository


class SQLAlchemyPortfolioSkinTransactionRepository(
     SQLAlchemyRepository[PortfolioSkinTransactionDTO, PortfolioSkinTransaction]
):
     model = PortfolioSkinTransaction