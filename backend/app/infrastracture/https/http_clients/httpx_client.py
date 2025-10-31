import httpx

from typing import Any, Literal

from fake_useragent import FakeUserAgent

from app.schemas import HttpResponseModel, RepeatRequestModel
from app.utils.logger import logger
from .abc import BaseHttpClient



class HttpxClient(BaseHttpClient):
     base_url: str = ""
     
     
     def __init__(self):
          self.ua = FakeUserAgent(platforms=["desktop"])
          
          
     def headers(self) -> dict[str, Any]:
          return {
               "User-Agent": self.ua.random,
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Connection": "keep-alive"
          }
          
               
     async def request(
          self,
          method: Literal["GET", "POST"],
          url: str,
          query_arguments: dict[str, Any] = {},
          headers: dict[str, Any] = {},
          data: dict[str, Any] = {},
          json_data: dict[str, Any] = {},
          cookies: dict[str, Any] = {},
          proxy: bool = False,
     ) -> HttpResponseModel:
          header = self.headers()
          if headers:
               header.update(headers)
               
          async with httpx.AsyncClient() as client:
               try:
                    response = await client.request(
                         method=method,
                         url=url,
                         data=data,
                         headers=header,
                         json=json_data,
                         params=query_arguments,
                         cookies=cookies
                    )
                    return HttpResponseModel(
                         status_code=response.status_code,
                         text=response.text
                    )
               except Exception as ex:
                    logger.http.error(
                         (
                              f"URL: {url}" 
                              f"\nQUERY: {query_arguments}" 
                              f"\nHEADER: {header}"
                              f"\nDATA: {data}"
                              f"\nJSON DATA: {json_data}"
                              f"\nCOOKIES: {cookies}"
                              f"\n\nSTATUS CODE: {response.status_code}"
                              f"\nTEXT: {response.text}"
                              f"\nEXCEPTION: {ex}"
                         )
                    )
                    return RepeatRequestModel(
                         status_code=response.status_code,
                         text=response.text
                    )