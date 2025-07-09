from pydantic import BaseModel



class NotifyData(BaseModel):
     skin_name: str
     percent: float
     old_time: str
     new_time: str
     
     
     @property
     def percent_valide(self) -> int:
          return self.percent if self.percent >= 0 else self.percent*-1