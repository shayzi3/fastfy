from typing import Protocol

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse

from app.schemas import SkinsPage, SkinHistoryTimePartModel, PaginateSkinsModel, SkinWithoutMetasModel
from app.schemas.dto import SkinDTO



class BaseSkinService(Protocol):
     
     
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
     ) -> SkinsPage[SkinDTO | SkinWithoutMetasModel]:
          ...
          
          
     async def skin_price_history(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          skin_name: str
     ) -> SkinHistoryTimePartModel | BaseResponse:
          ...