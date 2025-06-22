from typing import Protocol
from fastapi.responses import JSONResponse


class AbstractResponse(Protocol):
     description: str | None
     message: str | None
     status_code: int | None
     
     
     @classmethod
     def response(cls) -> JSONResponse:
          raise NotImplementedError