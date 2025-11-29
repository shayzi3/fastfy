from app.db.models import SkinPortfolioTransaction
from app.schemas.dto import SkinPortfolioTransactionDTO
from ..repository import SQLAlchemyRepository


class SQLAlchemySkinPortfolioTransactionRepository(
     SQLAlchemyRepository[SkinPortfolioTransactionDTO, SkinPortfolioTransaction]
):
     model = SkinPortfolioTransaction