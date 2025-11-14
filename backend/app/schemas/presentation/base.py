from typing_extensions import Self, Generic, TypeVar
from pydantic import BaseModel, PrivateAttr
from pydantic.main import IncEx



PM = TypeVar("PM", bound=BaseModel)



class BaseModelPresentation(BaseModel, Generic[PM]):
     _presentation: PM | None = PrivateAttr(default=None)
     
     def as_presentation(self, exclude: IncEx | None = None) -> Self | PM:
          if self._presentation:
               dump = self.model_dump(exclude=exclude, exclude_unset=True)
               return self._presentation.model_validate(dump)
          return self