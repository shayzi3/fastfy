from app.db.models import UserLikeSkin
from app.schemas.dto import UserLikeSkinDTO
from ..repository import SQLAlchemyRepository


class SQLAlchemyUserLikeSkinRepository(SQLAlchemyRepository[UserLikeSkinDTO, UserLikeSkin]):
     model = UserLikeSkin