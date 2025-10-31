from app.db.models import User
from app.schemas.dto import UserDTO
from ..reposiotry import SQLAlchemyRepository


class SQLAlchemyUserRepository(SQLAlchemyRepository[UserDTO, User]):
     model = User