from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.app.utils.logger import logger
from backend.app.api.v1.exceptions import exception_server_error



class LogMiddleware(BaseHTTPMiddleware):
     
     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
          logger.api.info(f"REQUEST FROM {request.client} TO {request.url}")
          
          try:
               return await call_next(request)
          except Exception as ex:
               logger.api.error(msg="error", exc_info=True)
               return await exception_server_error(request)