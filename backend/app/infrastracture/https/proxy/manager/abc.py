from typing import Protocol

from app.infrastracture.https.proxy.storage.abc import ProxyStorage



class BaseProxyManager(Protocol):
     def __init__(self, storage: ProxyStorage):
          self.storage = storage
     
     
     async def get_random_proxy(self) -> str:
          ...
          