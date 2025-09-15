from aiogram_tool.depend import Scope, dependency_scope

from bot.schemas.fastfy import DetailSchema
from bot.logger import logger
from bot.schemas.fastfy.enums import DetailStatus
from ..base import HttpClient



class AuthClient(HttpClient):
     
     async def steam_login(self) -> str:
          return self.url_builder(path="/auth/steam/login")
     
     
     async def telegram_processing(
          self,
          code: str,
          telegram_id: int,
          telegram_username: str
     ) -> DetailSchema:
          response = await self.request(
               method="POST",
               url=self.url_builder(path="/auth/telegram/processing"),
               query_arguments={"code": code},
               form_data_arguments={
                    "telegram_id": telegram_id,
                    "telegram_username": telegram_username
               }
          )
          if response.status_code == 400:
               return DetailSchema(detail="Введённый код несуществует!", status=DetailStatus.DONE)
          
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Telegram processing error {response.status_code} {response.obj.get('detail')}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.", status=DetailStatus.ERROR)
          
          return DetailSchema(detail="Регистрация прошла успешно.", status=DetailStatus.SUCCESS)
     
     
@dependency_scope(scope=Scope.APP)
async def get_auth_client() -> AuthClient:
     return AuthClient()
