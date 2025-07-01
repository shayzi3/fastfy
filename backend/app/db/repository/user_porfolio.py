from app.schemas import UserPortfolioModel
from app.db.models import UsersPortfolio

from .base import BaseRepository



class UserPortfolioRepository(
     BaseRepository[UserPortfolioModel, None]
):
     model = UsersPortfolio