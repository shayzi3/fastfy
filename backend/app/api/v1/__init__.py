from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from dishka.integrations.fastapi import DishkaRoute

from .routers.auth import auth_router
from .routers.user import user_router
from .routers.skin import skin_router
from .routers.portfolio import user_portfolio_router
from .routers.notification import notification_router
from .exceptions import exception_validation_error
from .middleware.logs import LogMiddleware


_routers = [
     APIRouter(route_class=DishkaRoute),
     auth_router,
     user_router,
     skin_router,
     user_portfolio_router,
     notification_router,
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