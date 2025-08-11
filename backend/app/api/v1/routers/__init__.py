from fastapi import FastAPI

from .auth.router import auth_router
from .user.router import user_router
from .skin.router import skin_router
from .user_portfolio.router import user_portfolio_router
from .notification.router import notification_router


_routers = [
     auth_router,
     user_router,
     skin_router,
     user_portfolio_router,
     notification_router
]


def include_routers(app: FastAPI):
     for route in _routers:
          app.include_router(route)