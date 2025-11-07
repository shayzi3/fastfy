from app.schemas.dto import UserDTO
from .mixin import Mixin




class UserMixin(Mixin[UserDTO]):
     dto = UserDTO