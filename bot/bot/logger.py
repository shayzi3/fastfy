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
     def bot(self) -> BaseLogger:
          return BaseLogger(
               name="BOT",
               filename=f"data/logs/bot/{self.__current_day()}.txt"
          )
          
     @property
     def notify_task(self) -> BaseLogger:
          return BaseLogger(
               name="NOTIFY TASK",
               filename=f"data/logs/notify_task/{self.__current_day()}.txt"
          )
          
     @property
     def fastfy_client(self) -> BaseLogger:
          return BaseLogger(
               name="FASTFY CLIENT",
               filename=f"data/logs/fastfy_client/{self.__current_day()}.txt"
          )
          

logger = FactoryBaseLogger()