from .slash_commands.user.router import slash_commands_user_router
from .states.user.router import state_user_router


__routers__ = [
     slash_commands_user_router,
     state_user_router
]