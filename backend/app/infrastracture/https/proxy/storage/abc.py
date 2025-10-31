from typing import Protocol



class ProxyStorage(Protocol):
          
     def _initial(self) -> None:
          ...
          
     async def delete_proxy(self, proxy: list[str], save: bool = False) -> None:
          ...
          
     async def add_proxy(self, proxy: list[str], save: bool = False) -> None:
          ...
          
     async def save_current_proxies(self) -> None:
          ...
          
     async def get_all_proxies(self) -> list[str]:
          ...