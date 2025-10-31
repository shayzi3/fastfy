from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from redis.asyncio import Redis

from app.core import my_config
from .exception import TestError





class ConnectionTests:
     # Tests for hosting
     
     async def start(self) -> None:
          await self.test_postgresql()
          await self.test_redis()
          
     
     @staticmethod
     async def test_postgresql() -> None:
          try:
               bind = create_async_engine(my_config.postgres_url)
               session = async_sessionmaker(bind=bind)
               
               async with session() as connection:
                    await connection.execute(text("SELECT 1"))
          except Exception as ex:
               raise TestError(f"Test failed: connect to PostgreSQL. {ex}")
               
     @staticmethod
     async def test_redis() -> None:
          try:
               connection = Redis(
                    host=my_config.redis_host,
                    port=my_config.redis_port,
                    password=my_config.redis_password
               )
               await connection.ping()
          except Exception as ex:
               raise TestError(f"Test failed: connection to Redis. {ex}")
               

test_connections = ConnectionTests()
          
               