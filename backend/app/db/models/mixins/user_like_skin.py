from app.schemas.dto import UserLikeSkinDTO
from .mixin import Mixin


class UserLikeSkinMixin(Mixin[UserLikeSkinDTO]):
     dto = UserLikeSkinDTO
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.market_hash_name