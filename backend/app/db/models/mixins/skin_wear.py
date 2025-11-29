from app.schemas.dto import SkinWearDTO
from .mixin import Mixin



class SkinWearMixin(Mixin[SkinWearDTO]):
     dto = SkinWearDTO
     
     