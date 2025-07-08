from enum import Enum


class UpdateMode(Enum):
     HIGH = "high"
     MEDIUM_WELL = "medium_well"
     MEDIUM = "medium"
     LOW = "low"
     
     
     @classmethod
     def filter_mode(cls, volume: int) -> "UpdateMode":
          if volume >= 20000:
               return cls.HIGH
          if volume >= 8000:
               return cls.MEDIUM_WELL
          if volume >= 2000:
               return cls.MEDIUM
          return cls.LOW
     
     
     def __str__(self):
          return self.value