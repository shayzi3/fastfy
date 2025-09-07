from typing import Annotated

from aiogram import Router
from aiogram.types import Message, URLInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram_tool.depend import Depend

from bot.schemas.fastfy import UserSchema, is_detail
from bot.utils.buttons.inline.user import profile_button, login_button, paginate_buttons
from bot.infrastracture.http.fastfy import FastFyClient, get_fastfy_client
from bot.utils.filters.user.state import SearchState


slash_commands_user_router = Router(name="slash_commands_user_router")



@slash_commands_user_router.message(CommandStart())
async def start(message: Message):
     await message.answer(
          f"👋 Привет {message.from_user.username}! Я помогу тебе отслеживать цены на предметы CS2!"
     )
     
     
@slash_commands_user_router.message(Command("account"))
async def account(
     message: Message,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     login_url = await client.auth.steam_login()
     await message.answer(
          text="Смена аккаунта",
          reply_markup=login_button(login_url)
     )
     
     
@slash_commands_user_router.message(Command("profile"))
async def profile(
     message: Message, 
     user: UserSchema
):
     await message.answer_photo(
          photo=URLInputFile(url=user.steam_avatar),
          caption=user.profile_text(),
          reply_markup=profile_button()
     )
     
     
@slash_commands_user_router.message(Command("clear"))
async def clear(
     message: Message,
     state: FSMContext
):
     current_state = await state.get_state()
     if current_state:
          await state.clear()
          return await message.answer("Событие пропущено.")
     await message.answer("Событий не найдено.")
     
     
@slash_commands_user_router.message(Command("portfolio"))
async def portfolio(
     message: Message,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)],
     user: UserSchema
):
     response = await client.user.get_user_portfolio(
          telegram_id=message.from_user.id,
          offset=0,
          limit=5
     )
     if is_detail(response):
          return await message.answer(text=response.detail)
          
     await message.answer(
          text=f"Портфолио для аккаунта: {user.steam_name}",
          reply_markup=paginate_buttons(
               skins=response,
               paginate_component="portfolio_skin"
          )
     )
     
     
     
@slash_commands_user_router.message(Command("search"))
async def search(
     message: Message,
     state: FSMContext
):
     await state.set_state(SearchState.query)
     await message.answer("Отправь название скина.")
     
     
@slash_commands_user_router.message(Command("steam_inventory"))
async def steam_inventory(
     message: Message
):
     ...
     
     
     

     
     
