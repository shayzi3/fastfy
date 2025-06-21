from pydantic import BaseModel



class TelegramData(BaseModel):
     telegram_id: int
     telegram_username: str
     
     
     
class SteamLoginUser(BaseModel):
     uuid: str
     steam_name: str
     steam_avatar: str