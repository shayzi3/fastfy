from typing import Callable, Any, Awaitable

from aiogram import Dispatcher
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.utils.buttons.inline.user import login_button
from bot.infrastracture.http.fastfy.base import HttpClient
from bot.infrastracture.http.fastfy import FastFyClient
from bot.infrastracture.http.fastfy.clients import AuthClient, SkinClient, UserClient
from bot.utils.filters.user.state import LoginState
from bot.alerts import AlertMessage
from bot.logger import logger




class UserMiddleware(BaseMiddleware):
     def __init__(self):
          self.client = HttpClient()
          self.fastfy_client = FastFyClient(
               auth_client=AuthClient(),
               skin_client=SkinClient(),
               user_client=UserClient()
          )
          
          
     async def __call__(
          self, 
          handler: Callable[[TelegramObject, dict[str, Any]], Awaitable],
          event: TelegramObject, 
          data: dict[str, Any]
     ):
          state: FSMContext = data.get("state")
          current_state = await state.get_state()
          if current_state == "LoginState:code":
               return await handler(event, data)
          
          dispatcher: Dispatcher = data.get("dispatcher")
          user: bool = (
               dispatcher.
               get("login_users", {}).
               get(event.from_user.id, False)
          )
          if user is False:
               response = await self.client.request(
                    method="GET",
                    url=self.client.url_builder("/user"),
                    query_arguments={"telegram_id": event.from_user.id}
               )
               if response.status_code == 200:
                    if "login_users" not in dispatcher.workflow_data:
                         dispatcher["login_users"] = {}
                    dispatcher["login_users"][event.from_user.id] = True
                    
               elif response.status_code in [400, 500, 422]:
                    await AlertMessage.send_alert(msg=f"Error in user-middleware {response.status_code} {response.obj.get('detail')}")
                    logger.bot.error(f"Middleware get user error {response.status_code} {response.obj.get('detail')}")
                    return await event.answer("Произошла ошибка. Повторите запрос позднее.")
               
               elif response.status_code in [401, 404]:
                    logger.bot.info(f"Register user {event.from_user.id} {event.from_user.username}")
                    
                    answer_event = event.message if isinstance(event, CallbackQuery) else event
                         
                    await answer_event.answer(
                         text=f"Привет {event.from_user.username}! Чтобы продолжить нужно пройти авторизацию."
                    )
                    
                    login_url = await self.fastfy_client.auth.steam_login()
                    await answer_event.answer(
                         text="Отправьте сюда код, полученный после входа в аккаунт.",
                         reply_markup=login_button(login_url)
                    )
                    return await state.set_state(LoginState.code)
          return await handler(event, data)
          