from app.schemas.dto import PortfolioSkinTransactionDTO



class BaseMathOperations:
     
     async def update_portfolio_skin_benefit(
          self,
          transactions: list[PortfolioSkinTransactionDTO],
          price_by_market_1pc: float,
          **kwargs
     ) -> float | None:
          if transactions:
               skin_count, skins_price = 0, 0
               for transaction in transactions:
                    skin_count += transaction.count
                    skins_price += transaction.count * transaction.buy_price
               
               avg_skins_price = skins_price / skin_count
               benefit = ((price_by_market_1pc - avg_skins_price) / avg_skins_price) * 100
               return round(benefit, 2)
          return None