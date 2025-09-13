from aiogram.utils.text_decorations import markdown_decoration

from bot.core.bot import bot
from bot.core.config import Config


class AlertMessage:
     
     @classmethod
     async def send_alert(cls, msg: str) -> None:
          async with bot as session:
               await session.send_message(
                    chat_id=Config.alert_chat,
                    text=markdown_decoration.quote(msg)
               )