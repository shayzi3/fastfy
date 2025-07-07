from pydantic import BaseModel, Field



class CreateUpdateSkin(BaseModel):
     quantity: int | None = Field(ge=1, default="null")
     buy_price: float | None = Field(ge=0, default="null")
     
     
     def non_nullable(self) -> dict[str, int | float]:
          return {
               key: value for key, value in self.model_dump().items()
               if value is not None
          }
          