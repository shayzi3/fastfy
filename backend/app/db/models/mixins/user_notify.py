from sqlalchemy.orm import selectinload

from app.schemas.dto import UserNotifyDTO
from .mixin import Mixin


class UserNotifyMixin(Mixin[UserNotifyDTO]):
     dto = UserNotifyDTO
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.created_at
     
     @classmethod
     def selectinload(cls):
          return [selectinload(cls.user)]