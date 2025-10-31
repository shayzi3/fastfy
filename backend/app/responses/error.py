from fastapi import status

from .base import Response



class SteamLoginError(Response):
     description = "Auth error of Steam"
     status_code = status.HTTP_400_BAD_REQUEST
     

class HttpError(Response):
     description = "Try Later"
     status_code = status.HTTP_403_FORBIDDEN
     
     
class TelegramLoginError(Response):
     description = "Invalid code"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class ServerError(Response):
     description = "Internal Server Error"
     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
     
     
class UserNotFoundError(Response):
     description = "User not found"
     status_code = status.HTTP_404_NOT_FOUND   
     
     
class SkinNotFoundError(Response):
     description = "Skin not found"
     status_code = status.HTTP_404_NOT_FOUND   
     
     
class SkinAlreadyExistsError(Response):
     description = "Skin already exists"
     status_code = status.HTTP_409_CONFLICT
     
     
class PortfolioEmptyError(Response):
     description = "Users portfolio empty"
     status_code = status.HTTP_403_FORBIDDEN
     
     
class SkinNotExistsError(Response):
     description = "Skin not exists"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class NotifyEmptyError(Response):
     description = "User notify not found"
     status_code = status.HTTP_404_NOT_FOUND
     
     
class OffsetError(Response):
     description = "The offset parameter must be divisible by limit without remainder."
     status_code = status.HTTP_403_FORBIDDEN
     
     
class SteamInventoryBlockedError(Response):
     description = "Impossible get user skins"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class JWTTokenExpireError(Response):
     description = "Истёк срок действия JWT токена."
     detail = "Истёк срок действия JWT токена."
     status_code = 401
     
     
class JWTTokenInvalidError(Response):
     description = "Invalid token"
     status_code = status.HTTP_401_UNAUTHORIZED
     
     
class ExchangeCodeInvalidError(Response):
     description = "Invalid code"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class ArgumentError(Response):
     description = "Not found arguments"
     status_code = status.HTTP_403_FORBIDDEN
     
     
class UserUpdateError(Response):
     description = "User doesn't update"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class TransactionNotFound(Response):
     description = "Transaction not found"
     status_code = status.HTTP_404_NOT_FOUND
     
     
class SkinTransactionError(Response):
     description = "Skin transaction error"
     status_code = status.HTTP_400_BAD_REQUEST