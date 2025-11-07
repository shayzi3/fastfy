from app.db.models import PortfolioSkinTransaction
from app.schemas.dto import PortfolioSkinTransactionDTO
from ..repository import SQLAlchemyRepository


class SQLAlchemyPortfolioSkinTransactionRepository(
     SQLAlchemyRepository[PortfolioSkinTransactionDTO, PortfolioSkinTransaction]
):
     model = PortfolioSkinTransaction