from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core import my_config


class Session:
     engine = create_async_engine(my_config.postgres_url, echo=False)
     session = async_sessionmaker(engine)
     
     
async def get_async_session():
     async with Session.session() as async_session:
          try:
               yield async_session
          except Exception as ex:
               await async_session.rollback()
               raise ex
          finally:
               await async_session.close()
               
               
               
session_asynccontext = asynccontextmanager(get_async_session)
               
