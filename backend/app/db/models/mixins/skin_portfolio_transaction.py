from app.schemas.dto import SkinPortfolioTransactionDTO
from .mixin import Mixin


class SkinPortfolioTransactionMixin(Mixin[SkinPortfolioTransactionDTO]):
     dto = SkinPortfolioTransactionDTO