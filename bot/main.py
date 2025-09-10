import asyncio

from aiogram_tool.depend import setup_depend_tool
from aiogram.types import BotCommand

from bot.core.bot import bot, dp
from bot.tasks import NotifyTask, run_tasks
from bot.handlers import __routers__
from bot.middleware import __middlewares__, include_middleware
from bot.logger import logger



@dp.startup()
async def startup() -> None:
     dp.include_routers(*__routers__)
     include_middleware(dp)
     setup_depend_tool(dispatcher=dp)
     
     await run_tasks(NotifyTask())
     
     await bot.set_my_commands(
          commands=[
               BotCommand(command="/start", description="Приветственное сообщение"),
               BotCommand(command="/account", description="Смена аккаунта"),
               BotCommand(command="/profile", description="Текущие данные акканута"),
               BotCommand(command="/clear", description="Очистка событий"),
               BotCommand(command="/portfolio", description="Скины текущего акканута"),
               BotCommand(command="/search", description="Поиск скинов"),
               BotCommand(command="/steam_inventory", description="Просмотр Steam скинов текущего аккаунта")
          ]
     )
     logger.bot.info("BOT STARTED")
     
     
@dp.shutdown()
async def shutdown() -> None:
     logger.bot.info("BOT SHUTDOWN")
     
     
     
async def main() -> None:
     await dp.start_polling(bot)
     
     
if __name__ == "__main__":
     asyncio.run(main())