from sqlalchemy.ext.asyncio import AsyncSession

from typing_extensions import Self

from app.repositories.abc_uow import BaseUnitOfWork
from app.db.session import async_session_maker
from app.utils.logger import logger
from .repo import (
     SQLAlchemyUserRepository,
     SQLAlchemyUserNotifyRepository,
     SQLAlchemySkinRepository,
     SQLAlchemySkinPriceHisoryRepository,
     SQLAlchemyUserPortfolioRepository,
     SQLAlchemyPortfolioSkinTransactionRepository,
     SQLAlchemyUserLikeSkinRepository,
     SQLAlchemySkinCollectionRepository
)





class SQLAlchemyUnitOfWork(BaseUnitOfWork):
     
     def __init__(self):
          self._session_factory = async_session_maker
          self._session: AsyncSession | None = None
          
     async def __aenter__(self) -> Self:
          if not self._session:
               self._session = self._session_factory()
          return self     
          
     async def __aexit__(self, *args) -> None:
          if args[0]:
               await self.rollback()
               logger.db_sqlalchemy.error(msg=args[1], exc_info=args[2])
          await self.close(*args)
     
     async def commit(self) -> None:
          if self._session:
               await self._session.commit()
          
     async def rollback(self) -> None:
          if self._session:
               await self._session.rollback() 
          
     async def close(self, *args) -> None:
          if self._session:
               await self._session.__aexit__(*args)
               self._session = None   
               
     @property
     def user_repo(self) -> SQLAlchemyUserRepository:
          return SQLAlchemyUserRepository(self._session)
     
     @property
     def user_notify_repo(self) -> SQLAlchemyUserNotifyRepository:
          return SQLAlchemyUserNotifyRepository(self._session)
     
     @property
     def skin_repo(self) -> SQLAlchemySkinRepository:
          return SQLAlchemySkinRepository(self._session)
     
     @property
     def skin_price_history_repo(self) -> SQLAlchemySkinPriceHisoryRepository:
          return SQLAlchemySkinPriceHisoryRepository(self._session)
     
     @property
     def user_skin_repo(self) -> SQLAlchemyUserPortfolioRepository:
          return SQLAlchemyUserPortfolioRepository(self._session)
     
     @property
     def user_like_skin_repo(self) -> SQLAlchemyUserLikeSkinRepository:
          return SQLAlchemyUserLikeSkinRepository(self._session)
     
     @property
     def skin_transaction_repo(self) -> SQLAlchemyPortfolioSkinTransactionRepository:
          return SQLAlchemyPortfolioSkinTransactionRepository(self._session)
     
     @property
     def skin_collection_repo(self) -> SQLAlchemySkinCollectionRepository:
          return SQLAlchemySkinCollectionRepository(self._session)
     
          
          