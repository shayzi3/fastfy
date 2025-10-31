from typing import Protocol

from .abc_repo.abc_user import BaseUserRepository
from .abc_repo.abc_skin import BaseSkinRepository
from .abc_repo.abc_skin_price_history import BaseSkinPriceHistoryRepository
from .abc_repo.abc_user_portfolio import BaseUserPortfolioRepository
from .abc_repo.abc_user_notify import BaseUserNotifyRepository
from .abc_repo.abc_portfolio_skin_transaction import BasePortfolioSkinTransactionRepository
from .abc_repo.abc_user_like_skin import BaseUserLikeSkinRepository



class BaseUnitOfWork(Protocol):
     user_repo: BaseUserRepository
     skin_repo: BaseSkinRepository
     skin_price_history_repo: BaseSkinPriceHistoryRepository
     user_portfolio_repo: BaseUserPortfolioRepository
     portoflio_skin_transaction_repo: BasePortfolioSkinTransactionRepository
     user_like_skin_repo: BaseUserLikeSkinRepository
     user_notify_repo: BaseUserNotifyRepository
     
     
     def __init__(self):
          self._session_factory = None
          self._session = None
     
     
     async def __aenter__(self) -> None:
          ...
          
          
     async def __aexit__(self) -> None:
          ...
          
     
     async def commit(self) -> None:
          ...
          
          
     async def rollback(self) -> None:
          ...
          
          
     async def close(self) -> None:
          ...
          