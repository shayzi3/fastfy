from uuid import UUID
from datetime import datetime
from pydantic import BaseModel



class UserModel(BaseModel):
     uuid: UUID
     steam_id: int
     steam_name: str
     steam_avatar: str
     created_at: datetime
     telegram_id: int | None = None
     telegram_username: str | None = None
     
     
     
          
class TokenPayload(BaseModel):
     uuid: str
     iat: datetime
     exp: datetime
     
     


class SteamLoginUser(BaseModel):
     uuid: str
     steam_name: str
     steam_avatar: str