from enum import Enum


class UpdateModeEnum(Enum):
     HIGH = "HIGH"
     MEDIUM_WELL = "MEDIUM_WELL"
     MEDIUM = "MEDIUM"
     LOW = "LOW"
     
     
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
     

class NotifyTypeEnum(Enum):
     INFO = "INFO"
     SKIN = "SKIN"
     
     
class OrderByPaginateSkinsEnum(Enum):
     PRICE = "price"
     POPULAR = "sell_by_last_update"
     PRICE_LAST_1_DAY = "price_last_1_day"
     PRICE_LAST_7_DAY = "price_last_7_day"
     PRICE_LAST_30_DAY = "price_last_30_day"
     
     
     
class OrderByPaginatePortfolioSkinsEnum(Enum):
     BENEFIT = "benefit"
     
     

     
class OrderByModeEnum(Enum):
     DESC = "desc"
     ASC = "asc"
     
     
     
class UserNotifyEnum(Enum):
     ON = "on"
     OFF = "off"
     
     
     
class WhereConditionEnum(Enum):
     EQ = "="
     GT = ">"
     GE = ">="
     LT = "<"
     LE = "<="
     ILIKE = "ilike"
     IN = "in"
     
     