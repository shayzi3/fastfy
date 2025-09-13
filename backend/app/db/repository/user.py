from app.schemas import UserModel
from app.db.models import Users

from .base import BaseRepository



class UserRepository(BaseRepository[UserModel, None]):
     model = Users


