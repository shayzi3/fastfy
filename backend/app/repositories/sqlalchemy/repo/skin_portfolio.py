from app.schemas.dto import SkinPortfolioDTO
from app.db.models import SkinPortfolio
from ..repository import SQLAlchemyRepository


class SQLAlchemySkinPortfolioRepository(
     SQLAlchemyRepository[SkinPortfolioDTO, SkinPortfolio]
):
     model = SkinPortfolio