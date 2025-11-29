from typing import Protocol

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse
from app.repositories.abc_condition import BaseWhereCondition

from app.schemas import (
     SkinsPage, 
     SkinHistoryTimePartModel, 
     PaginateSkinsModel
)
from app.schemas.dto import SkinDTO



class BaseSkinService(Protocol):
     def __init__(self, condition: BaseWhereCondition):
          self.condition = condition
          
     
     async def get_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          skin_name: str
     ) -> SkinDTO | BaseResponse:
          ...
          

     async def search_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[SkinDTO]:
          ...
          
          
     async def skin_price_history(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          skin_name: str
     ) -> SkinHistoryTimePartModel | BaseResponse:
          ...