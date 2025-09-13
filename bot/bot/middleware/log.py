from typing import Callable, Any, Awaitable

from aiogram.types import TelegramObject
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from bot.logger import logger
from bot.alerts import AlertMessage



class LogMiddleware(BaseMiddleware):
     
     async def __call__(
          self, 
          handler: Callable[[TelegramObject, dict[str, Any]], Awaitable], 
          event: TelegramObject, 
          data: dict[str, Any]
     ):
          router_name = getattr(data.get("event_router"), "name", "")
          callback = getattr(data.get("handler"), "callback", "")
          
          if callback:
               callback = getattr(callback, "__name__", "")
               
          logger.bot.info(
               f"USER {event.from_user.id}~{event.from_user.username} ROUTER {router_name} CALLBACK {callback}"
          )
          try:
               return await handler(event, data)
          except Exception as ex:
               logger.bot.error(msg=str(ex), exc_info=True)
               await AlertMessage.send_alert(msg=f"Error {str(ex)}")
               return await event.answer("Произошла ошибка. Повторите попытку позже.")