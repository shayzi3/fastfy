from enum import Enum
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
     
     
class OrderByPaginateSkinsEnum(Enum):
     PRICE = "price"
     PRICE_LAST_1_DAY = "price_last_1_day"
     PRICE_LAST_30_DAY = "price_last_30_day"
     EMPTY = "empty"
     
     def __str__(self):
          return self.value
     
     
class OrderByModeEnum(Enum):
     DESC = "desc"
     ASC = "asc"
     EMPTY = "empty"
     
     def __str__(self):
          return self.value
     
     
class UserNotifyEnum(Enum):
     ON = "on"
     OFF = "off"
     EMPTY = "empty"
     
     def __str__(self):
          return self.value
     
     

     
UpdateMode = UpdateModeEnum()
NotifyType = NotifyTypeEnum()

     
     