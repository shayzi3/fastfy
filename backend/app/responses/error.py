
from .base import BaseResponse


class SteamLoginError(BaseResponse):
     description = "Error when login with Steam"
     message = "SteamLoginError"
     status_code = 403
     

     
class HttpError(BaseResponse):
     description = "Error when server send http request"
     message = "TryLater"
     status_code = 500
     
     
class TokenError(BaseResponse):
     description = "Invalid token"
     message = "TokenError"
     status_code = 401
     
     
class TelegramProcessError(BaseResponse):
     description = "Link not valid"
     message = "OldLink"
     status_code = 400