from typing import Any
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
     pydantic_model = None
     
     
     def dump(self) -> dict[str, Any]:
          return self.__dict__