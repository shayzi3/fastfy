import logging

from datetime import datetime


class BaseLogger(logging.Logger):
     def __init__(self, name: str, filename: str):
          super().__init__(name, logging.INFO)
          
          handler = logging.FileHandler(filename=filename)
          formatter = logging.Formatter(
               "%(levelname)s %(asctime)s [%(filename)s (%(funcName)s)] %(message)s"
          )
          handler.setFormatter(formatter)
          self.addHandler(handler)
          
          
          
class FactoryBaseLogger:
     
     def __current_day(self) -> str:
          return datetime.now().strftime("%Y-%m-%d")
     
     
     @property
     def api(self) -> BaseLogger:
          return BaseLogger(
               name="API",
               filename=f"data/logs/api/{self.__current_day()}.txt"
          )
          
     @property
     def http_steam(self) -> BaseLogger:
          return BaseLogger(
               name="HTTP_STEAM",
               filename=f"data/logs/http_steam/{self.__current_day()}.txt"
          )
          
     @property
     def task_update_notify(self) -> BaseLogger:
          return BaseLogger(
               name="TASK_UPDATE_NOTIFY",
               filename=f"data/logs/task_update_notify/{self.__current_day()}.txt"
          )
          
     @property
     def task_price_at_days(self) -> BaseLogger:
          return BaseLogger(
               name="TASK_PRICE_AT_DAYS",
               filename=f"data/logs/task_price_at_days/{self.__current_day()}.txt"
          )
          
          
logger = FactoryBaseLogger()