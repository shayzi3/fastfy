from app.schemas.dto import PortfolioSkinTransactionDTO
from .mixin import Mixin


class UserPortfolioMixin(Mixin[PortfolioSkinTransactionDTO]):
     dto = PortfolioSkinTransactionDTO