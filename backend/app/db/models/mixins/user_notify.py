from app.schemas.dto import UserNotifyDTO
from .mixin import Mixin


class UserNotifyMixin(Mixin[UserNotifyDTO]):
     dto = UserNotifyDTO