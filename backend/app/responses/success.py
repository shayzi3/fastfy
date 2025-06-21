from .base import BaseResponse



class SteamLoginSuccess(BaseResponse):
     message = "SteamLoginSuccess"
     status_code = 200
     
     
class TelegramProcessSuccess(BaseResponse):
     message = "TelegramProcessSuccess"
     status_code = 200