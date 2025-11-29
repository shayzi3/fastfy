from typing import Protocol

from typing_extensions import Self

from .abc_repo import (
     BaseUserRepository,
     BaseSkinRepository,
     BaseSkinWearRepository,
     BaseSkinPriceHistoryRepository,
     BaseSkinPortfolioRepository,
     BaseSkinPortfolioTransactionRepository,
     BaseUserLikeSkinRepository,
     BaseUserNotifyRepository,
     BaseSkinCollectionRepository
)



class BaseUnitOfWork(Protocol):
     user_repo: BaseUserRepository
     skin_repo: BaseSkinRepository
     skin_wear_repo: BaseSkinWearRepository
     skin_price_history_repo: BaseSkinPriceHistoryRepository
     skin_portfolio_repo: BaseSkinPortfolioRepository
     skin_portoflio_transaction_repo: BaseSkinPortfolioTransactionRepository
     user_like_skin_repo: BaseUserLikeSkinRepository
     user_notify_repo: BaseUserNotifyRepository
     skin_collection_repo: BaseSkinCollectionRepository

     
     def __init__(self):
          self._session_factory = None
          self._session = None
          self._cached_repository = {}
     
     
     async def __aenter__(self) -> Self:
          return self
          
          
     async def __aexit__(self) -> None:
          ...
          
     
     async def commit(self) -> None:
          ...
          
          
     async def rollback(self) -> None:
          ...
          
          
     async def close(self) -> None:
          ...
          