from app.schemas.dto import SkinPriceHistoryDTO
from .mixin import Mixin


class SkinPriceHistoryMixin(Mixin[SkinPriceHistoryDTO]):
     dto = SkinPriceHistoryDTO