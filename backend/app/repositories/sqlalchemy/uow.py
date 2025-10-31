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
     users_repo: SQLAlchemyUserRepository
     users_notify_repo: SQLAlchemyUserNotifyRepository
     skins_repo: SQLAlchemySkinRepository
     skins_price_history_repo: SQLAlchemySkinPriceHisoryRepository
     user_skins_repo: SQLAlchemyUserPortfolioRepository
     users_likes_skins_repo: SQLAlchemyUserLikeSkinRepository
     skins_transactions_repo: SQLAlchemyPortfolioSkinTransactionRepository

     
     def __init__(self):
          self._session_factory = async_session_maker
          self._session: AsyncSession | None = None
          
          
     async def __aenter__(self) -> None:
          self._session = self._session_factory()
          
          self.users_repo = SQLAlchemyUserRepository(self._session)
          self.users_notify_repo = SQLAlchemyUserNotifyRepository(self._session)
          self.skins_repo = SQLAlchemySkinRepository(self._session)
          self.skins_price_history_repo = SQLAlchemySkinPriceHisoryRepository(self._session)
          self.user_skins_repo = SQLAlchemyUserPortfolioRepository(self._session)  
          self.users_likes_skins_repo = SQLAlchemyUserLikeSkinRepository(self._session)
          self.skins_transactions_repo = SQLAlchemyPortfolioSkinTransactionRepository(self._session)        
          
          
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
          
          