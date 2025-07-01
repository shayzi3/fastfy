from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import my_config


class Session:
     engine = create_async_engine(my_config.postgres_url, echo=False)
     session = async_sessionmaker(engine)