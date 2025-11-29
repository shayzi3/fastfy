from app.schemas.dto import SkinPortfolioDTO
from .mixin import Mixin


class SkinPortfolioMixin(Mixin[SkinPortfolioDTO]):
     dto = SkinPortfolioDTO