import asyncio

from bot.schemas.fastfy import UserNotifySchema, is_detail
from bot.core.bot import bot
from bot.infrastracture.http.fastfy import FastFyClient



class BaseNotifyTask:
     def __init__(self):
          self.__client = FastFyClient()
     
     
     async def _process(self) -> None:
          response = await self.__client.user.get_all_users_notifies()
          if is_detail(response):
               return
          
          notifies = []
          for notify in response:
               notifies.append(
                    self.__send_notify_process(notify)
               )
               
          if notifies:
               await asyncio.gather(*notifies)
          
          
     async def __send_notify_process(self, notify: UserNotifySchema) -> None:
          async with bot as session:
               await session.send_message(
                    chat_id=notify.user.telegram_id,
                    text=notify.text
               )