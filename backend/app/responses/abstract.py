from typing import Protocol
from fastapi.responses import JSONResponse
from fastapi import HTTPException


class AbstractResponse(Protocol):
     detail: str | None
     status_code: int | None
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          raise NotImplementedError
     
     
     @classmethod
     def exec(cls) -> HTTPException:
          raise NotImplementedError
     
     
     @classmethod
     def schema(cls) -> dict[int, dict]:
          raise NotImplementedError