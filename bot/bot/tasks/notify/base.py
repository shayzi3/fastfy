import asyncio

from aiogram.enums import ParseMode
from aiogram.utils.text_decorations import markdown_decoration

from bot.schemas.fastfy import UserNotifySchema
from bot.infrastracture.http.fastfy import FastFyClient
from bot.core.bot import bot
from bot.logger import logger



class BaseNotifyTask:
     def __init__(self):
          self.__client = FastFyClient()
     
     
     async def _process(self) -> None:
          logger.notify_task.info("START PROCESS")
          
          response = await self.__client.user.get_all_users_notifies()
          if response is None:
               return logger.notify_task.error("Error when get all users notifies. Watch fastfy_client log")
          
          notifies = []
          for notify in response:
               notifies.append(self.__send_notify_process(notify))
               
          if notifies:
               await asyncio.gather(*notifies)
          
          
     async def __send_notify_process(self, notify: UserNotifySchema) -> None:
          async with bot as session:
               await session.send_message(
                    chat_id=notify.user.telegram_id,
                    text=markdown_decoration.quote(notify.text),
                    parse_mode=ParseMode.MARKDOWN_V2
               )