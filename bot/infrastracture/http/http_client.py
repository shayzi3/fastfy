import aiohttp



class HttpClient:
     def __init__(self):
          self.base_url = "https://hbcbva-185-247-185-62.ru.tuna.am/api/v1"
          
          
     async def verify_processid(
          self, 
          processid: str, 
          tg_id: int, 
          tg_username: str
     ) -> bool:
          url = self.base_url + f"/auth/telegram/processing?processid={processid}"
          data = {
               "telegram_id": tg_id,
               "telegram_username": tg_username
          }
          async with aiohttp.ClientSession() as session:
               result = await session.post(url=url, json=data)
               if result.status != 200:
                    return False
          return True