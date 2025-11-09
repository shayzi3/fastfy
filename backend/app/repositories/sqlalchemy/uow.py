from sqlalchemy.ext.asyncio import AsyncSession

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
     SQLAlchemyUserLikeSkinRepository
)





class SQLAlchemyUnitOfWork(BaseUnitOfWork):
     
     def __init__(self):
          self._session_factory = async_session_maker
          self._session: AsyncSession | None = None
          
     async def __aenter__(self) -> None:
          if not self._session:
               self._session = self._session_factory()          
          
     async def __aexit__(self, *args) -> None:
          if args[0]:
               await self.rollback()
               logger.db.error(msg=args[1], exc_info=args[2])
          await self.close()
     
     async def commit(self) -> None:
          if self._session:
               await self._session.commit()
          
     async def rollback(self) -> None:
          if self._session:
               await self._session.rollback() 
          
     async def close(self) -> None:
          if self._session:
               await self._session.close()  
               self._session = None   
               
     @property
     def users_repo(self) -> SQLAlchemyUserRepository:
          return SQLAlchemyUserRepository(self._session)
     
     @property
     def users_notify_repo(self) -> SQLAlchemyUserNotifyRepository:
          return SQLAlchemyUserNotifyRepository(self._session)
     
     @property
     def skins_repo(self) -> SQLAlchemySkinRepository:
          return SQLAlchemySkinRepository(self._session)
     
     @property
     def skins_price_history_repo(self) -> SQLAlchemySkinPriceHisoryRepository:
          return SQLAlchemySkinPriceHisoryRepository(self._session)
     
     @property
     def user_skins_repo(self) -> SQLAlchemyUserPortfolioRepository:
          return SQLAlchemyUserPortfolioRepository(self._session)
     
     @property
     def users_likes_skins_repo(self) -> SQLAlchemyUserLikeSkinRepository:
          return SQLAlchemyUserLikeSkinRepository(self._session)
     
     @property
     def skins_transactions_repo(self) -> SQLAlchemyPortfolioSkinTransactionRepository:
          return SQLAlchemyPortfolioSkinTransactionRepository(self._session)
     
     
          
          