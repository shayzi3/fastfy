from typing import Annotated
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram_tool.depend import Depend

from bot.schemas.fastfy.enums import DetailStatus
from bot.infrastracture.http.fastfy import get_fastfy_client, FastFyClient
from bot.utils.filters.user.state import LoginState


state_user_router = Router(name="state_user_router")



@state_user_router.message(LoginState.code)
async def login_state_code(
     message: Message, 
     state: FSMContext,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     response = await client.auth.telegram_processing(
          code=message.text,
          telegram_id=message.from_user.id,
          telegram_username=message.from_user.username
     )
     if response.status in [DetailStatus.SUCCESS, DetailStatus.ERROR]:
          await state.clear()
          
     await message.answer(text=response.detail)
     
     
     
     


