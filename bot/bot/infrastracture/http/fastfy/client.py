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