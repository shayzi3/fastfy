from .auth import AuthClient
from .skin import SkinClient
from .user import UserClient




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