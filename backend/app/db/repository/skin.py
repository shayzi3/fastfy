from app.schemas import SkinModel
from app.db.models import Skins

from .base import BaseRepository



class SkinRepository(BaseRepository[SkinModel, None]):
     model = Skins