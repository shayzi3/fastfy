from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.responses import ServerError



async def exception_validation_error(
     _: Request, 
     exc: RequestValidationError
) -> JSONResponse:
     error_body = exc.errors()[0]
     
     return JSONResponse(
          content={
               "detail": f"Input '{error_body.get('input')}'. {error_body.get('msg')}"
          },
          status_code=422
     )
     
     
async def exception_server_error(_: Request) -> JSONResponse:
     return ServerError.response()