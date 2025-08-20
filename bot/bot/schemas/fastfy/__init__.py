from typing import TypeVar
from pydantic import BaseModel

from .schema import (
     DetailSchema,
     SkinSchema,
     ResponseObjectSchema,
     SkinsOnPageSchema,
     SkinPriceHistorySchema
)


T = TypeVar("T", bound=BaseModel)



def is_detail(obj: T) -> bool:
     return getattr(obj, "is_detail", None) is True