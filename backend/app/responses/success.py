from .base import Response




class TelegramLoginSuccess(Response):
     detail = "Telegram account linked successfully"          
     
class SkinCreateSuccess(Response):
     description = "Skin created"
     
     
class SkinDeleteSuccess(Response):
     description = "Skin deleted"
     
     
class SkinChangeSuccess(Response):
     description = "Data changed"
     
     
class UserUpdateSuccess(Response):
     description = "Data updated"
     
     
class SkinTransactionSuccess(Response):
     description = "Skin transaction success"