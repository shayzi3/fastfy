from aiogram_tool.depend import Scope, dependency_scope

from .clients.auth import AuthClient
from .clients.skin import SkinClient
from .clients.user import UserClient




class FastFyClient:
     
     @property
     def auth(self) -> AuthClient:
          return AuthClient()
     
     
     @property
     def skin(self) -> SkinClient:
          return SkinClient()
     
     
     @property
     def user(self) -> UserClient:
          return UserClient()
     
     
     
@dependency_scope(scope=Scope.APP)
async def get_fastfy_client() -> FastFyClient:
     return FastFyClient()