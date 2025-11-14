import logging
import pytz

from datetime import datetime

from app.core import my_config
from .timezone import moscow_datetime, moscow_timezone



class MoscowTimezoneFormatter(logging.Formatter):
     def formatTime(self, record, datefmt = None):
          dt = datetime.fromtimestamp(record.created, tz=pytz.utc)
          dt = dt.astimezone(moscow_timezone)
          
          if datefmt:
               return dt.strftime(datefmt)
          return dt.isoformat()



class BaseLogger(logging.Logger):
     def __init__(self, name: str, filename: str):
          super().__init__(name, logging.INFO)
          
          handler = logging.FileHandler(filename=filename)
          formatter = MoscowTimezoneFormatter(
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
     def db_sqlalchemy(self) -> BaseLogger:
          return BaseLogger(
               name="DBAlchemy",
               filename=f"{my_config.data_path}/db/sqlalchemy/{self.__current_day()}.txt"
          )
          
     
          
          
logger = FactoryBaseLogger()