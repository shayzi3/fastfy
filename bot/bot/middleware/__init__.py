from aiogram import Dispatcher

from .user import UserMiddleware
from .log import LogMiddleware


__middlewares__ = [
     LogMiddleware,
     UserMiddleware
]


def include_middleware(dp: Dispatcher) -> None:
     for event in dp.resolve_used_update_types():
          observer = dp.observers.get(event)
          
          for middle in __middlewares__:
               observer.middleware(middle())