from abc import ABC, abstractmethod



class AbstractTask(ABC):
     
     @abstractmethod
     async def run(self) -> None:
          raise NotImplementedError
     
     
async def run_tasks(*tasks: AbstractTask) -> None:
     for task in tasks:
          await task.run()