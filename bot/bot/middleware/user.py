from typing import Callable, Any, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from bot.infrastracture.http.fastfy.base import HttpClient
from bot.schemas.fastfy import UserSchema



class UserMiddleware(BaseMiddleware):
     def __init__(self):
          self.client = HttpClient()
          
          
     async def __call__(
          self, 
          handler: Callable[[TelegramObject, dict[str, Any]], Awaitable],
          event: TelegramObject, 
          data: dict[str, Any]
     ):
          response = await self.client.request(
               method="GET",
               url=self.client.url_builder("/user"),
               query_arguments={"telegram_id": event.from_user.id}
          )
          if response.status_code in [400, 500, 422]:
               return event.answer("Произошла ошибка. Повторите запрос позднее.")
          
          elif response.status_code in [401, 404]:
               return event.answer(
                    text="Требуется вход в аккаунт.",
                    reply_markup=...
               )
               
          data.update({"user": UserSchema.model_validate(response.obj)})
          return await handler(event, data)
          