import asyncio

from typing import ParamSpec, TypeVar, Callable
from functools import wraps

from app.schemas import RepeatRequestModel
from app.responses import HttpError
from app.utils.logger import logger, BaseLogger


P = ParamSpec("P")
T = TypeVar("T")


def retry(max_attemps: int, delay: float = 1, log_category: str = "") -> Callable[[Callable[P, T]], Callable[P, T]]:
     def repeater(func: Callable[P, T]) -> Callable[P, T]:
          @wraps(func)
          async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
               attemp = 0
               logger_by_category: BaseLogger = getattr(logger, log_category, None)
               while attemp <= max_attemps:
                    await asyncio.sleep(0 if attemp == 0 else delay)
                    
                    try:
                         result = await func(*args, **kwargs)
                         if isinstance(result, RepeatRequestModel):
                              if logger_by_category:
                                   logger_by_category.info(f"REPEAT {args} {kwargs} RESPONSE {result}")
                              attemp += 1
                              continue
                         return result
                    except Exception as ex:
                         if logger_by_category:
                              logger_by_category.error(f"REPEAT {args} {kwargs} RESPONSE {result} EXCEPTION {ex}")
                         attemp += 1
                         
               if logger_by_category:
                    logger_by_category.error(f"MAX REPEAT {args} {kwargs} LAST RESULT {result}")
               return HttpError
          return wrapper
     return repeater