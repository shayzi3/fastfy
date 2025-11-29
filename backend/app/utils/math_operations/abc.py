from typing import Protocol

from app.schemas.dto import SkinPortfolioTransactionDTO



class BaseMathOperations(Protocol):
     
     async def update_portfolio_skin_benefit(
          self,
          transactions: list[SkinPortfolioTransactionDTO],
          price_by_market_1pc: float
     ) -> float | None:
          ...