from app.schemas import SkinModel, SkinRelModel
from app.db.models import Skins

from .base import BaseRepository



class SkinRepository(BaseRepository[SkinModel, SkinRelModel]):
     model = Skins