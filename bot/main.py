import asyncio

from aiogram_tool.depend import setup_depend_tool

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
     
     logger.bot.info("BOT STARTED")
     
     
@dp.shutdown()
async def shutdown() -> None:
     logger.bot.info("BOT SHUTDOWN")
     
     
     
async def main() -> None:
     await dp.start_polling(bot)
     
     
if __name__ == "__main__":
     asyncio.run(main())