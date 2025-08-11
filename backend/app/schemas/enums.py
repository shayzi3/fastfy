from enum import Enum, auto


class UpdateMode(Enum):
     HIGH = auto()
     MEDIUM_WELL = auto()
     MEDIUM = auto()
     LOW = auto()
     
     
     @classmethod
     def filter_mode(cls, volume: int) -> "UpdateMode":
          if volume >= 20000:
               return cls.HIGH
          if volume >= 8000:
               return cls.MEDIUM_WELL
          if volume >= 2000:
               return cls.MEDIUM
          return cls.LOW
     
     
     
class NotifyType(Enum):
     INFO = auto()
     SKIN = auto()
     
     