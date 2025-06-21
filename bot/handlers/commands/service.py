from infrastracture.http import HttpClient
from infrastracture.redis import RedisPool


class CommandsService:
     def __init__(self):
          self.http_client = HttpClient()
          self.redis = RedisPool()
          
          
     async def start(
          self,
          token: str,
          tg_id: int,
          tg_username: str
     ) -> bool:
          processid = await self.redis.get(token)
          if processid is not None:
               await self.redis.delete(token)
               result = await self.http_client.verify_processid(
                    processid=processid,
                    tg_id=tg_id,
                    tg_username=tg_username
               )
               return result
          return False
     
     
async def get_commands_service() -> CommandsService:
     return CommandsService()