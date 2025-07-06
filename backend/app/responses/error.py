from .base import BaseResponse



class SteamLoginError(BaseResponse):
     detail = "SteamLoginError"
     status_code = 403
     

class HttpError(BaseResponse):
     detail = "TryLater"
     status_code = 500
     
     
class TokenError(BaseResponse):
     detail = "TokenError"
     status_code = 401
     
     
class TelegramProcessError(BaseResponse):
     detail = "OldLink"
     status_code = 400
     
     
class UserNotFoundError(BaseResponse):
     detail = "UserNotFound"
     status_code = 404
     
     
class ArgumentError(BaseResponse):
     detail = "ArgumentError"
     status_code = 403
     
     
class SkinNotFoundError(BaseResponse):
     detail = "SkinNotFound"
     status_code = 404
     
     
class SkinPortfolioAlreadyExists(BaseResponse):
     detail = "SkinPortfolioAlreadyExists"
     status_code = 400
     
     
class PortfolioEmpty(BaseResponse):
     detail = "PortfolioEmpty"
     status_code = 400