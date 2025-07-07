from .base import BaseResponse




class TelegramProcessSuccess(BaseResponse):
     detail = "TelegramProcessSuccess"
     status_code = 200
     
     
class PortfolioSkinCreateSuccess(BaseResponse):
     detail = "PortfolioSkinCreateSuccess"
     status_code = 200
     
     
class PortfolioSkinSoonCreate(BaseResponse):
     detail = "PortfolioSkinSoonCreate"
     status_code = 200
     
     
class SkinDeleteSuccess(BaseResponse):
     detail = "SkinDeleteSuccess"
     status_code = 200
     
     
     
class SkinChangeSuccess(BaseResponse):
     detail = "SkinChangeSuccess"
     status_code = 200
     
     
class NotifyUpdateSuccess(BaseResponse):
     detail = "NotifyUpdateSuccess"
     status_code = 200