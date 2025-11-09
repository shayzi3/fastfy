from app.schemas.dto import PortfolioSkinTransactionDTO
from .mixin import Mixin


class PortfolioSkinTransactionMixin(Mixin[PortfolioSkinTransactionDTO]):
     dto = PortfolioSkinTransactionDTO