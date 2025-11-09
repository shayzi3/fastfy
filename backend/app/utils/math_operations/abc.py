from typing import Protocol

from app.schemas.dto import PortfolioSkinTransactionDTO



class BaseMathOperations(Protocol):
     
     async def update_portfolio_skin_benefit(
          self,
          transactions: list[PortfolioSkinTransactionDTO],
          price_by_market_1pc: float
     ) -> float | None:
          ...