from dishka import Provider, Scope, provide

from backend.app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.core.security.abc import BaseJWTSecurity

from app.infrastracture.cache.redis import CacheRedis
from app.infrastracture.https.clients.steam import SteamClient
from backend.app.infrastracture.https.http_clients.httpx_client import HttpxClient
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from app.infrastracture.openid.steam import SteamOpenID
from app.core.security import JWTSecurity
from app.services.abc import (
     BaseAuthService,
     BaseUserService,
     BaseSkinService,
     BasePortfolioService,
     BaseUserLikeSkinsService,
     BaseSkinTransactionService,
     BaseNotificationService
)
from app.services import (
     AuthService,
     NotificationService,
     PortfolioService,
     UserService,
     SkinService,
     UserLikeSkinsService,
     SkinTransactionService
)



class MainProvider(Provider):

     @provide(scope=Scope.REQUEST)
     def cache(self) -> Cache:
          return CacheRedis()
     
     
     @provide(scope=Scope.REQUEST)
     def unit_of_work(self) -> BaseUnitOfWork:
          return SQLAlchemyUnitOfWork()
     
     
     @provide(scope=Scope.APP)
     def jwt_security(self) -> BaseJWTSecurity:
          return JWTSecurity()
     
     
     @provide(scope=Scope.APP)
     def auth_service(self) -> BaseAuthService:
          return AuthService(
               steam_client=SteamClient(http_client=HttpxClient()),
               openid=SteamOpenID(),
               jwt_security=JWTSecurity()
          )
     
     
     @provide(scope=Scope.APP)
     def user_service(self) -> BaseUserService:
          return UserService(
               steam_client=SteamClient(
                    http_client=HttpxClient()
               )
          )
     
     @provide(scope=Scope.APP)
     def skin_service(self) -> BaseSkinService:
          return SkinService()
     
     
     @provide(scope=Scope.APP)
     def notification_service(self) -> BaseNotificationService:
          return NotificationService()
     
     
     @provide(scope=Scope.APP)
     def portfolio_service(self) -> BasePortfolioService:
          return PortfolioService()
     
     
     @provide(scope=Scope.APP)
     def user_like_skins_service(self) -> BaseUserLikeSkinsService:
          return UserLikeSkinsService()
     
     
     @provide(scope=Scope.APP)
     def skin_transactions_service(self) -> BaseSkinTransactionService:
          return SkinTransactionService()
     