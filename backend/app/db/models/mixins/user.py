from typing import Any

from app.schemas.dto import UserDTO
from .mixin import Mixin




class UserMixin(Mixin[UserDTO]):
     dto = UserDTO
     
     
     @classmethod
     def returning(cls) -> Any:
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.created_at
     