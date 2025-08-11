from app.schemas import UserSkinModel, UserSkinRelModel
from app.db.models import UsersSkins

from .base import BaseRepository



class UserSkinRepository(
     BaseRepository[UserSkinModel, UserSkinRelModel]
):
     model = UsersSkins
     
     
     
          
          