from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core import my_config


class Session:
     engine = create_async_engine(my_config.postgres_url, echo=False)
     session = async_sessionmaker(engine)
     
     
     
async def get_async_session():
     async with Session.session() as async_session:
          try:
               yield async_session
          finally:
               await async_session.close()