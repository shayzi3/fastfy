from app.schemas import UserPortfolioRelModel, UserPortfolioModel
from app.db.models import UsersPortfolio

from .base import BaseRepository



class UserPortfolioRepository(
     BaseRepository[UserPortfolioModel, UserPortfolioRelModel]
):
     model = UsersPortfolio