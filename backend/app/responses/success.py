from typing import Any
from fastapi.responses import JSONResponse

from .base import BaseResponse



class ResponseSuccess(JSONResponse):
     def __init__(self, result: Any):
          super().__init__(
               content={"detail": result},
               status_code=200
          )

     
class TelegramProcessSuccess(BaseResponse):
     detail = "TelegramProcessSuccess"
     status_code = 200