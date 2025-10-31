from app.schemas.dto import SkinDTO
from .mixin import Mixin


class SkinMixin(Mixin[SkinDTO]):
     dto = SkinDTO
     
     
     @classmethod
     def returning(cls):
          return cls.skin_name
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     @classmethod
     def paginate_query_column(cls):
          return cls.market_hash_name