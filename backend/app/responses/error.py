from .base import BaseResponse



class SteamLoginError(BaseResponse):
     description = "Произошла ошибка при авторизации через Steam."
     detail = "Произошла ошибка при авторизации через Steam."
     status_code = 400
     

class HttpError(BaseResponse):
     description = "Повторите попытку позже."
     detail = "Повторите попытку позже."
     status_code = 403
     
     
class TelegramLoginError(BaseResponse):
     description = "Недействительный код."
     detail = "Недействительный код."
     status_code = 400
     
     
class ServerError(BaseResponse):
     description = "Ошибка на стороне сервера."
     detail = "Ошибка на стороне сервера."
     status_code = 500
     
     
class AuthError(BaseResponse):
     description = "Нужно пройти повторную авторизацию."
     status_code = 401
     
     
class SecretTokenError(BaseResponse):
     description = "Недействительный секретный код."
     detail = "Недействительный секретный код."
     status_code = 400
     
     
class UserNotFoundError(BaseResponse):
     description = "Запрашивемый пользователь не найден."
     status_code = 404     
     
     
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
     
     
class OffsetError(BaseResponse):
     description = "Параметр offset должен делиться на 5 без остатка."
     status_code = 403
     
     
class SteamInventoryBlocked(BaseResponse):
     description = "Невозможно получить скины пользователя."
     detail = "Невозможно получить скины пользователя."
     status_code = 400