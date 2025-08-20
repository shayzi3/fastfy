from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from .service import CommandsService


command_router = Router()



@command_router.message(CommandStart(deep_link=True))
@inject
async def start(
     message: Message, 
     command: CommandObject,
     service: FromDishka[CommandsService]
):
     result = await service.start(
          token=command.args,
          tg_id=message.from_user.id,
          tg_username=message.from_user.username
     )
     if result is False:
          return await message.answer("Ссылка устарела.")
     await message.answer("Аккаунт успешно привязан.")