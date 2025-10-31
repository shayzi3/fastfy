from app.schemas.dto import SkinPriceHistoryDTO
from .mixin import Mixin


class SkinPriceHistoryMixin(Mixin[SkinPriceHistoryDTO]):
     dto = SkinPriceHistoryDTO
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.timestamp