from app.db.models import SkinCollection
from app.schemas.dto import SkinCollectionDTO
from ..repository import SQLAlchemyRepository


class SQLAlchemySkinCollectionRepository(
     SQLAlchemyRepository[SkinCollectionDTO, SkinCollection]
):
     model = SkinCollection