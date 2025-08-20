from bot.schemas.fastfy import DetailSchema
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
          return DetailSchema.model_validate(response.obj)
