from app.schemas import UserModel, UserRelModel
from app.db.models import Users

from .base import BaseRepository



class UserRepository(BaseRepository[UserModel, UserRelModel]):
     model = Users


