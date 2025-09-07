from typing import Annotated

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_tool.depend import Depend

from bot.schemas.fastfy import is_detail
from bot.schemas.fastfy.enums import DetailStatus
from bot.utils.filters.user.state import UserPercentState
from bot.utils.filters.user.callback_data import Skin, Paginate
from bot.infrastracture.http.fastfy import FastFyClient, get_fastfy_client
from bot.utils.buttons.inline.user import paginate_buttons
from bot.utils.compress import CompressName


callback_user_router = Router(name="user_callback_router")


@callback_user_router.callback_query(F.data == "empty")
async def empty_button(query: CallbackQuery):
     await query.answer()


@callback_user_router.callback_query(F.data == "change_user_percent")
async def change_percent_user(
     query: CallbackQuery,
     state: FSMContext
):
     await query.message.answer("Отправь число от 1 до 100")
     await state.set_state(UserPercentState.percent)
     await query.answer()
     
     
@callback_user_router.callback_query(Paginate.filter(F.mode == "skin_search"))
async def paginate_skin_search(
     query: CallbackQuery,
     callback_data: Paginate,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     if callback_data.vector == "left" and callback_data.offset == 0:
          return await query.answer("Дальше листать не получится.")
     
     offset_plus = 5 if callback_data.vector == "right" else -5
     response = await client.skin.search_skins(
          offset=callback_data.offset + offset_plus,
          limit=5,
          query=callback_data.query
     )
     if is_detail(response):
          if response.status == DetailStatus.DONE:
               return await query.answer("Дальше листать не получится.")
          return await query.answer(text=response.detail)
          
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=paginate_buttons(
               skins=response, 
               query=callback_data.query,
               offset=callback_data.offset + offset_plus,
               paginate_component="skin_search"
          )
     )
     
     
@callback_user_router.callback_query(Skin.filter(F.mode == "skin_search"))
async def click_skin_search(
     query: CallbackQuery,
     callback_data: Skin,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     response = await client.user.create_skin_at_user_portfolio(
          telegram_id=query.from_user.id,
          skin_name=CompressName.compress(
               skin_name=callback_data.skin_name,
               mode="from"
          )
     )
     await query.answer(text=response.detail)
     
     
     
@callback_user_router.callback_query(Paginate.filter(F.mode == "portfolio_skin"))
async def paginate_portfolio_skin(
     query: CallbackQuery,
     callback_data: Paginate,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     if callback_data.vector == "left" and callback_data.offset == 0:
          return await query.answer("Дальше листать не получится.")
          
     offset_plus = 5 if callback_data.vector == "right" else -5
     response = await client.user.get_user_portfolio(
          telegram_id=query.from_user.id,
          offset=callback_data.offset + offset_plus,
          limit=5
     )
     if is_detail(response):
          if response.status == DetailStatus.DONE:
               return await query.answer("Дальше листать не получится.")
          return await query.answer(text=response.detail)
     
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=paginate_buttons(
               skins=response,
               paginate_component="portfolio_skin",
               offset=callback_data.offset + offset_plus
          )
     )
     
     
@callback_user_router.callback_query(Skin.filter(F.mode == "portfolio_skin"))
async def click_portfolio_skin(
     query: CallbackQuery,
     callback_data: Skin,
     client: Annotated[FastFyClient, Depend(get_fastfy_client)]
):
     await query.answer("Button works")