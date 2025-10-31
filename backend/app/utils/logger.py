import logging

from app.core import my_config
from .timezone import moscow_datetime, moscow_timezone



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
          return moscow_datetime().strftime("%Y-%m-%d")
     
     
     @property
     def api(self) -> BaseLogger:
          return BaseLogger(
               name="API",
               filename=f"{my_config.data_path}/api/{self.__current_day()}.txt"
          )
          
     @property
     def http(self) -> BaseLogger:
          return BaseLogger(
               name="HTTP",
               filename=f"{my_config.data_path}/https/http/{self.__current_day}.txt"
          )
          
     @property
     def http_steam(self) -> BaseLogger:
          return BaseLogger(
               name="HTTP_STEAM",
               filename=f"{my_config.data_path}/https/steam/{self.__current_day()}.txt"
          )
          
     @property
     def task_update_notify(self) -> BaseLogger:
          return BaseLogger(
               name="TASK_UPDATE_NOTIFY",
               filename=f"{my_config.data_path}/tasks/update_notify/{self.__current_day()}.txt"
          )
          
     @property
     def task_price_at_days(self) -> BaseLogger:
          return BaseLogger(
               name="TASK_PRICE_AT_DAYS",
               filename=f"{my_config.data_path}/tasks/price_at_days/{self.__current_day()}.txt"
          )
          
     @property
     def task_new_skins(self) -> BaseLogger:
          return BaseLogger(
               name="TASK_NEW_SKINS",
               filename=f"{my_config.data_path}/tasks/new_skins/{self.__current_day()}.txt"
          )
          
     @property
     def db(self) -> BaseLogger:
          return BaseLogger(
               name="DB",
               filename=f"{my_config.data_path}/db/{self.__current_day()}.txt"
          )
          
     
          
          
logger = FactoryBaseLogger()