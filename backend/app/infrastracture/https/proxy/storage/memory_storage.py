# import aiofiles

# from .abc import ProxyStorage



# class ProxyMemoryStorage(ProxyStorage):
#      proxies = []
     
#      def __init__(self, proxies_file: str):
#           self.proxies_file = proxies_file
#           self._initial()
          
#      def _initial(self) -> None:
#           with open(self.proxies_file, "r") as file:
#                data = file.read()
#                if data:
#                     proxies = data.split("\n")
#                     self.proxies = list(set([proxy.strip() for proxy in proxies if proxy]))
          
#      async def add_proxy(self, proxy: list[str], save: bool = False) -> None:
#           unique_proxy = list(set(proxy))
#           for addr in unique_proxy:
#                if addr not in self.proxies:
#                     self.proxies.append(addr)
#           if save:
#                await self.save_current_proxies()
               
#      async def delete_proxy(self, proxy: list[str], save: bool = False) -> None:
#           for addr in proxy:
#                try:
#                     self.proxies.remove(addr)
#                except ValueError:
#                     continue
#           if save:
#                await self.save_current_proxies()
               
#      async def save_current_proxies(self):
#           async with aiofiles.open(self.proxies_file, "w") as file:
#                writable = "\n".join(self.proxies)
#                await file.write(writable)
               
               
#      async def get_all_proxies(self) -> list[str]:
#           return self.proxies
          
          