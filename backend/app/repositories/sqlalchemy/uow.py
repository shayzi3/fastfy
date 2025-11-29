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
     SQLAlchemySkinPortfolioRepository,
     SQLAlchemySkinPortfolioTransactionRepository,
     SQLAlchemyUserLikeSkinRepository,
     SQLAlchemySkinCollectionRepository,
     SQLAlchemySkinWearRepository
)





class SQLAlchemyUnitOfWork(BaseUnitOfWork):
     
     def __init__(self):
          self._session_factory = async_session_maker
          self._session: AsyncSession | None = None
          self._cached_repository = {}
          
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
               self._cached_repository.clear()
               
     @property
     def user_repo(self) -> SQLAlchemyUserRepository:
          cache_key = "user_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemyUserRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def user_notify_repo(self) -> SQLAlchemyUserNotifyRepository:
          cache_key = "user_notify_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemyUserNotifyRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def skin_repo(self) -> SQLAlchemySkinRepository:
          cache_key = "skin_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def skin_wear_repo(self) -> SQLAlchemySkinWearRepository:
          cache_key = "skin_wear_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinWearRepository(self._session)
          return self._cached_repository[cache_key] 
     
     @property
     def skin_price_history_repo(self) -> SQLAlchemySkinPriceHisoryRepository:
          cache_key = "skin_price_history_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinPriceHisoryRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def skin_portfolio_repo(self) -> SQLAlchemySkinPortfolioRepository:
          cache_key = "skin_portfolio_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinPortfolioRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def user_like_skin_repo(self) -> SQLAlchemyUserLikeSkinRepository:
          cache_key = "user_like_skin"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemyUserLikeSkinRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def skin_portfolio_transaction_repo(self) -> SQLAlchemySkinPortfolioTransactionRepository:
          cache_key = "skin_portfolio_transaction_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinPortfolioTransactionRepository(self._session)
          return self._cached_repository[cache_key]
     
     @property
     def skin_collection_repo(self) -> SQLAlchemySkinCollectionRepository:
          cache_key = "skin_collection_repo"
          
          if cache_key not in self._cached_repository:
               self._cached_repository[cache_key] = SQLAlchemySkinCollectionRepository(self._session)
          return self._cached_repository[cache_key]     
          
          