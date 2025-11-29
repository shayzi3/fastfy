from app.db.models import SkinWear
from app.schemas.dto import SkinWearDTO
from ..repository import SQLAlchemyRepository



class SQLAlchemySkinWearRepository(
     SQLAlchemyRepository[SkinWearDTO, SkinWear]
):
     model = SkinWear