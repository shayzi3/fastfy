from pydantic import BaseModel


class UpdateModeEnum(BaseModel):
     HIGH: str = "HIGH"
     MEDIUM_WELL: str = "MEDIUM_WELL"
     MEDIUM: str = "MEDIUM"
     LOW: str = "LOW"
     
     
     def filter_mode(
          self, 
          volume: int,
          last_price: float | None, 
          new_price: float
     ) -> str:
          if last_price is None:
               if volume >= 8000:
                    return "LOW"
               
               elif volume >= 5000:
                    return "MEDIUM_WELL"
               
               elif volume >= 2000:
                    return "MEDIUM"
               return "HIGH"
               
          price_change_percent = ((new_price - last_price) / last_price) * 100
          if (price_change_percent >= 10) or (price_change_percent <= -10):
               return "HIGH"
          
          elif (price_change_percent >= 6) or (price_change_percent <= -6):
               return "MEDIUM_WELL"
          
          elif (price_change_percent >= 3) or (price_change_percent <= -3):
               return "MEDIUM"
          return "LOW"
     

     

class NotifyTypeEnum(BaseModel):
     INFO: str = "INFO"
     SKIN: str = "SKIN"
     
     
UpdateMode = UpdateModeEnum()
NotifyType = NotifyTypeEnum()

     
     