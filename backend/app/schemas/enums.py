from enum import Enum



class HistoryFilter(Enum):
     ALL = "all"
     YEAR = "year"
     MONTH = "month"
     DAY = "day"
     
     
     @property
     def day(self) -> int:
          return {
               "year": 365,
               "month": 30,
               "day": 1
          }[self.value]