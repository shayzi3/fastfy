from typing import Protocol
from fastapi.responses import JSONResponse
from fastapi import HTTPException


class BaseResponse(Protocol):
     description: str
     status_code: int
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          ...
     
     
     @classmethod
     def exec(cls) -> HTTPException:
          ...
     
     
     @classmethod
     def schema(cls) -> dict[int, dict]:
          ...
     