from app.schemas.dto import UserPortfolioDTO
from app.db.models import UserPortfolio
from ..repository import SQLAlchemyRepository


class SQLAlchemyUserPortfolioRepository(
     SQLAlchemyRepository[UserPortfolioDTO, UserPortfolio]
):
     model = UserPortfolio