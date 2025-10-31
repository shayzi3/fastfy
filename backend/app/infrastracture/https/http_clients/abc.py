from typing import Protocol, Any

from app.schemas import HttpResponseModel
from app.infrastracture.https.proxy.manager.abc import BaseProxyManager




class BaseHttpClient(Protocol):
     base_url: str = ""
     
     
     def __init__(self, proxy_mamanger: BaseProxyManager):
          self.proxy_manager = proxy_mamanger
     
     
     def headers(self) -> dict[str, Any]:
          ...
     
     
     async def request(
          self,
          method: str,
          url: str,
          query_arguments: dict[str, Any] = {},
          headers: dict[str, Any] = {},
          data: dict[str, Any] = {},
          json_data: dict[str, Any] = {},
          cookies: dict[str, Any] = {}
     ) -> HttpResponseModel:
          ...
          