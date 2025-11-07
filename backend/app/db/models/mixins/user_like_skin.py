from app.schemas.dto import UserLikeSkinDTO
from .mixin import Mixin


class UserLikeSkinMixin(Mixin[UserLikeSkinDTO]):
     dto = UserLikeSkinDTO