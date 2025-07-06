from pydantic import BaseModel, Field



class CreateUpdateSkin(BaseModel):
     quantity: int = Field(ge=1, default=0)
     buy_price: float = Field(ge=0, default=-1)
     
     
     @property
     def non_nullable(self) -> dict[str, int | float]:
          values = {}
          if self.quantity != 0:
               values["quantity"] = self.quantity
               
          if self.buy_price != -1:
               values["buy_price"] = self.buy_price
          return values