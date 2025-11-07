from app.schemas.dto import SkinDTO
from app.db.models import Skin
from ..repository import SQLAlchemyRepository


class SQLAlchemySkinRepository(SQLAlchemyRepository[SkinDTO, Skin]):
     model = Skin