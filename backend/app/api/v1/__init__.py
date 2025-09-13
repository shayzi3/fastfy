from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .routers.auth.router import auth_router
from .routers.user.router import user_router
from .routers.skin.router import skin_router
from .routers.user_portfolio.router import user_portfolio_router
from .routers.notification.router import notification_router
from .routers.exceptions import exception_validation_error
from .middleware.logs import LogMiddleware


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
_middlewares = [
     LogMiddleware,
]


def include_routers(app: FastAPI) -> None:
     for route in _routers:
          app.include_router(route)
          
          
def include_exception_handlers(app: FastAPI) -> None:
     for error, exce_handler in _exceptions:
          app.add_exception_handler(error, exce_handler)
          
          
def include_middleware(app: FastAPI) -> None:
     for middleware in _middlewares:
          app.add_middleware(middleware)