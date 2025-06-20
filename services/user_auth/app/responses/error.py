
from .base import BaseResponse


class SteamLoginError(BaseResponse):
     message = "SteamLoginError"
     status_code = 403
     
     
class SteamAlreadyExistsError(BaseResponse):
     message = "SteamAlreadyExists"
     status_code = 409
     
     
class HttpError(BaseResponse):
     message = "TryLater"
     status_code = 500
     
     
class TokenError(BaseResponse):
     message = "TokenError"
     status_code = 401