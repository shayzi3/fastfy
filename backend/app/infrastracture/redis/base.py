from redis.asyncio import Redis



class RedisPool(Redis):
     def __init__(self) -> None:
          super().__init__(decode_responses=True)
          
     
     
async def get_redis_session():
     async with RedisPool() as pool:
          try:
               yield pool
          finally:
               await pool.aclose()