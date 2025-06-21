from typing import Any
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
     pydantic_model = None
     pydantic_rel_model = None