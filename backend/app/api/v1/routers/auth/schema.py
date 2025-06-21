from pydantic import BaseModel



class TelegramData(BaseModel):
     telegram_id: int
     telegram_username: str
     