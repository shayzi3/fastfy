from sqlalchemy.orm import selectinload

from app.schemas.dto import PortfolioSkinTransactionDTO
from .mixin import Mixin


class UserPortfolioMixin(Mixin[PortfolioSkinTransactionDTO]):
     dto = PortfolioSkinTransactionDTO
     
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     @classmethod
     def selectinload(cls):
          return [selectinload(cls.skin), selectinload(cls.user)]