from fastapi import status

from .base import Response



class LoginError(Response):
     description = "Login error"
     status_code = status.HTTP_400_BAD_REQUEST


class HttpError(Response):
     description = "Try Later"
     status_code = status.HTTP_403_FORBIDDEN
     
     
class ServerError(Response):
     description = "Internal Server Error"
     status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
     
     
class NotFoundError(Response):
     description = "Data not found"
     status_code = status.HTTP_404_NOT_FOUND
     
     
class DataAlreadyExistsError(Response):
     description = "Data already exists"
     status_code = status.HTTP_409_CONFLICT
     
     
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
     
     
class InvalidCodeError(Response):
     description = "Invalid code"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class ArgumentError(Response):
     description = "Not found arguments"
     status_code = status.HTTP_403_FORBIDDEN
     
     
class UpdateError(Response):
     description = "Update error"
     status_code = status.HTTP_400_BAD_REQUEST
     
     
class DataNotExistsError(Response):
     description = "Data not exists error"
     status_code = status.HTTP_403_FORBIDDEN
     

class DeleteError(Response):
     description = "Delete error"
     status_code = status.HTTP_400_BAD_REQUEST