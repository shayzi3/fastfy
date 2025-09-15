from typing import Annotated
from aiogram.types import Message
from aiogram import Router, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram_tool.depend import Depend

from bot.schemas.fastfy.enums import DetailStatus
from bot.schemas.fastfy import is_detail
from bot.infrastracture.http.fastfy import get_fastfy_client, FastFyClient
from bot.utils.filters.user.state import LoginState, UserPercentState, SearchState
from bot.utils.buttons.inline.user import paginate_buttons


state_user_router = Router(name="state_user_router")



@state_user_router.message(LoginState.code)
async def login_state_code(
     message: Message, 
     state: FSMContext,
     dispatcher: Dispatcher,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     response = await client.auth.telegram_processing(
          code=message.text,
          telegram_id=message.from_user.id,
          telegram_username=message.from_user.username
     )
     if response.status in [DetailStatus.SUCCESS, DetailStatus.ERROR]:
          await state.clear()
          
     if response.status == DetailStatus.SUCCESS:
          if "login_users" not in dispatcher.workflow_data:
               dispatcher["login_users"] = {}
          dispatcher["login_users"][message.from_user.id] = True
     await message.answer(text=response.detail)
     
     
@state_user_router.message(LoginState.code_change_account)
async def change_account_code(
     message: Message,
     state: FSMContext,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     await message.answer("В разработке...")
     
     
@state_user_router.message(UserPercentState.percent)
async def user_change_percent(
     message: Message,
     state: FSMContext,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     if not message.text.isdigit():
          return await message.answer("Это не число!")
     
     percent = int(message.text)
     if percent <= 0 or percent > 100:
          return await message.answer("Число должно быть от 1 до 100!")
     
     response = await client.user.change_percent_user(
          telegram_id=message.from_user.id,
          percent=percent
     )
     await message.answer(text=response.detail)
     await state.clear()
     
     
@state_user_router.message(SearchState.query)
async def skins_search(
     message: Message,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     if len(message.text.encode()) > 40:
          return await message.answer("Слишком длинный запрос.")
     
     response = await client.skin.search_skins(
          offset=0,
          limit=5,
          query=message.text
     )
     if is_detail(response):
          return await message.answer(text=response.detail)
     
     await message.answer(
          text=f"Результат по запросу: {message.text}",
          reply_markup=paginate_buttons(
               skins=response,
               query=message.text,
               paginate_component="skin_search"
          )
     )
     
     
     
        
     
     
     
     


