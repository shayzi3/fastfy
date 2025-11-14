from dishka import Provider, Scope, provide
from fastapi import Request

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.core.security.abc import BaseJWTSecurity

from app.infrastracture.cache.redis import CacheRedis
from app.infrastracture.https.clients.steam import SteamClient
from app.infrastracture.https.http_clients.httpx_client import HttpxClient
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from app.infrastracture.openid.steam import SteamOpenID
from app.core.security import JWTSecurity
from app.schemas import JWTTokenPayloadModel
from app.repositories.sqlalchemy.condition import SQLAlchemyWhereCondition
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
     def cache(self, request: Request) -> Cache:
          return CacheRedis()
     
     @provide(scope=Scope.REQUEST)
     def unit_of_work(self, request: Request) -> BaseUnitOfWork:
          return SQLAlchemyUnitOfWork()
     
     @provide(scope=Scope.REQUEST)
     async def jwt_security(self, request: Request, jwt_sec_ins: BaseJWTSecurity) -> JWTTokenPayloadModel:
          return await jwt_sec_ins(request=request)
     
     @provide(scope=Scope.APP)
     def jwt_security_instance(self) -> BaseJWTSecurity:
          return JWTSecurity()
     
     @provide(scope=Scope.APP)
     def auth_service(self, jwt_sec_ins: BaseJWTSecurity) -> BaseAuthService:
          return AuthService(
               steam_client=SteamClient(http_client=HttpxClient()),
               openid=SteamOpenID(),
               jwt_security=jwt_sec_ins,
               condition=SQLAlchemyWhereCondition
          )
     
     @provide(scope=Scope.APP)
     def user_service(self) -> BaseUserService:
          return UserService(
               steam_client=SteamClient(
                    http_client=HttpxClient()
               ),
               condition=SQLAlchemyWhereCondition
          )
     
     @provide(scope=Scope.APP)
     def skin_service(self) -> BaseSkinService:
          return SkinService(condition=SQLAlchemyWhereCondition)
     
     
     @provide(scope=Scope.APP)
     def notification_service(self) -> BaseNotificationService:
          return NotificationService(condition=SQLAlchemyWhereCondition)
     
     
     @provide(scope=Scope.APP)
     def portfolio_service(self) -> BasePortfolioService:
          return PortfolioService(condition=SQLAlchemyWhereCondition)
     
     
     @provide(scope=Scope.APP)
     def user_like_skins_service(self) -> BaseUserLikeSkinsService:
          return UserLikeSkinsService(condition=SQLAlchemyWhereCondition)
     
     
     @provide(scope=Scope.APP)
     def skin_transactions_service(self) -> BaseSkinTransactionService:
          return SkinTransactionService(condition=SQLAlchemyWhereCondition)