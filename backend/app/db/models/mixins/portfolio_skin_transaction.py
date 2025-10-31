from sqlalchemy.orm import selectinload

from app.schemas.dto import PortfolioSkinTransactionDTO
from .mixin import Mixin


class PortfolioSkinTransactionMixin(Mixin[PortfolioSkinTransactionDTO]):
     dto = PortfolioSkinTransactionDTO
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.when_buy