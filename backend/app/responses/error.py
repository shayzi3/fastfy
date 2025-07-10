from .base import BaseResponse



class SteamLoginError(BaseResponse):
     description = "Произошла ошибка при авторизации через Steam"
     status_code = 403
     

class HttpError(BaseResponse):
     description = "Произошла ошибка при отправке запроса внешнему сервису."
     detail = "TryLater"
     status_code = 500
     
     
     
class TokenError(BaseResponse):
     description = "Ошибка авторизации."
     status_code = 401
     
     
     
class TelegramProcessError(BaseResponse):
     description = "Ошибка привязки Telegram аккаунта. Ссылка устарела."
     detail = "OldLink"
     status_code = 400
     
     
     
class UserNotFoundError(BaseResponse):
     description = "Пользователь не найден."
     status_code = 404
     
     
     
class ArgumentError(BaseResponse):
     description = "В запросе не хватает аргументов."
     status_code = 403
     
     
     
class SkinNotFoundError(BaseResponse):
     description = "Скин не найден."
     status_code = 404
     
     
     
class SkinPortfolioAlreadyExists(BaseResponse):
     description = "Скин в портфолио польвателя уже существует."
     status_code = 400
     
     
     
class PortfolioEmpty(BaseResponse):
     description = "Портфолио пользователя пустое."
     status_code = 400
     
     
     
class SkinNotExists(BaseResponse):
     description = "Скин не существует."
     status_code = 400
     
     
     
class NotifyEmpty(BaseResponse):
     description = "Уведомления пользователя не найдены."
     status_code = 404
     
     
class RequestTimeoutError(BaseResponse):
     detail = "RequestTimeoutError: time"
     description = "Превышен лимит запросов."
     status_code = 429
     