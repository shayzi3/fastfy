from dishka import Provider, provide, Scope

from handlers.commands.service import CommandsService



class DependencyProvider(Provider):
     
     
     @provide(scope=Scope.APP)
     async def get_commands_service(self) -> CommandsService:
          return CommandsService()