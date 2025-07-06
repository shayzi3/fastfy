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