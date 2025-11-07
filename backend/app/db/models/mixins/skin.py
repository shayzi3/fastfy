from app.schemas.dto import SkinDTO
from .mixin import Mixin


class SkinMixin(Mixin[SkinDTO]):
     dto = SkinDTO