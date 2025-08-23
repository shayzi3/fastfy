from aiogram_tool.depend import Depend
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


slash_commands_user_router = Router(name="slash_commands_user_router")



@slash_commands_user_router.message(CommandStart())
async def start(message: Message):
     await message.answer(
          f"👋 Привет {message.from_user.username}! Я помогу тебе отслеживать цены на предметы CS2!"
     )
     
     
