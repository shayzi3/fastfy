from .base import BaseResponse




class TelegramLoginSuccess(BaseResponse):
     detail = "Телеграмм акааунт привязан успешно."
     description = "Телеграмм аккаунт привязан успешно."
          
     
class PortfolioSkinCreateSuccess(BaseResponse):
     description = "Скин в портфолио создан успешно."
     
     
class PortfolioSkinSoonCreate(BaseResponse):
     description = "Скин в портфолии скоро будет добавлен."
     status_code = 202
     
     
class SkinDeleteSuccess(BaseResponse):
     description = "Скин удалён успешно."
     
     
class SkinChangeSuccess(BaseResponse):
     description = "Данные скины успешно изменены"
     
     
class NotifyUpdateSuccess(BaseResponse):
     description = "Уведомление создано успешно."
     
     
class UserUpdateSuccess(BaseResponse):
     description = "Данные пользователя успешно обновлены."