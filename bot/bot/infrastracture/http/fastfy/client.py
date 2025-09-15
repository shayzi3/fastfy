from typing import Annotated
from aiogram_tool.depend import Scope, dependency_scope, Depend

from .clients.auth import AuthClient, get_auth_client
from .clients.skin import SkinClient, get_skin_client
from .clients.user import UserClient, get_user_client




class FastFyClient:
     def __init__(
          self,
          auth_client: AuthClient,
          skin_client: SkinClient,
          user_client: UserClient
     ):
          self.auth = auth_client
          self.skin = skin_client
          self.user = user_client
     
     
     
@dependency_scope(scope=Scope.APP)
async def get_fastfy_client(
     auth_client: Annotated[AuthClient, Depend(get_auth_client)],
     skin_client: Annotated[SkinClient, Depend(get_skin_client)],
     user_client: Annotated[UserClient, Depend(get_user_client)]
) -> FastFyClient:
     return FastFyClient(
          auth_client=auth_client,
          skin_client=skin_client,
          user_client=user_client
     )