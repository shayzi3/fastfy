from enum import Enum, auto


class UpdateMode(Enum):
     HIGH = auto()
     MEDIUM_WELL = auto()
     MEDIUM = auto()
     LOW = auto()
     
     
     @classmethod
     def filter_mode(
          cls, 
          volume: int,
          last_price: float | None, 
          new_price: float
     ) -> "UpdateMode":
          if last_price is None:
               if volume >= 8000:
                    return cls.LOW
               
               elif volume >= 5000:
                    return cls.MEDIUM_WELL
               
               elif volume >= 2000:
                    return cls.MEDIUM
               return cls.HIGH
               
          price_change_percent = ((new_price - last_price) / last_price) * 100
          if (price_change_percent >= 10) or (price_change_percent <= -10):
               return cls.HIGH
          
          elif (price_change_percent >= 6) or (price_change_percent <= -6):
               return cls.MEDIUM_WELL
          
          elif (price_change_percent >= 3) or (price_change_percent <= -3):
               return cls.MEDIUM
          return cls.LOW
     
     
class NotifyType(Enum):
     INFO = auto()
     SKIN = auto()
     
     