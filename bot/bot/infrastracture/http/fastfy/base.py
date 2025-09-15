import httpx

from typing import Literal, Any

from bot.core.config import Config
from bot.schemas.fastfy import ResponseObjectSchema



class HttpClient:
     
     
     @staticmethod
     def headers() -> dict[str, Any]:
          return {
               "Secret-Bot-Token": Config.fastfy_secret_bot_token
          }
          
          
     @staticmethod
     def url_builder(path: str) -> str:
          if path[0] != "/":
               raise ValueError("path should started with '/'")
          return Config.fastfy_base_url + path
     
     
     async def request(
          self,
          method: Literal["GET", "POST", "PATCH", "DELETE"],
          url: str,
          query_arguments: dict[str, Any] = {},
          form_data_arguments: dict[str, Any] = {}
     ) -> ResponseObjectSchema:
          async with httpx.AsyncClient() as session:
               try:
                    response = await session.request(
                         method=method,
                         url=url,
                         data=form_data_arguments,
                         params=query_arguments,
                         headers=self.headers()
                    )
                    return ResponseObjectSchema(
                         status_code=response.status_code,
                         obj=response.json()
                    )
               except Exception as ex:
                    return ResponseObjectSchema(
                         status_code=500,
                         obj={"detail": "Произошла ошибка. Повторите попытку позже."}
                    )