from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .auth.router import auth_router
from .user.router import user_router
from .skin.router import skin_router
from .user_portfolio.router import user_portfolio_router
from .notification.router import notification_router
from .exceptions import exception_validation_error


_routers = [
     auth_router,
     user_router,
     skin_router,
     user_portfolio_router,
     notification_router
]

_exceptions = [
     (RequestValidationError, exception_validation_error),
]


def include_routers(app: FastAPI) -> None:
     for route in _routers:
          app.include_router(route)
          
          
def include_exception_handlers(app: FastAPI) -> None:
     for error, exce_handler in _exceptions:
          app.add_exception_handler(error, exce_handler)