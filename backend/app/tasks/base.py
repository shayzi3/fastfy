from abc import ABC, abstractmethod




class AbstarctTask(ABC):
     
     
     @abstractmethod
     async def run(self) -> None:
          raise NotImplementedError
     
     
     
async def run_tasks(*tasks: AbstarctTask) -> None:
     for task in tasks:
          await task.run()