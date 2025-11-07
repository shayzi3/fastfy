from datetime import timedelta
from typing import Type

from app.services.abc.abc_skin_service import BaseSkinService
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse
from app.repositories.abc_condition import BaseWhereCondition
from app.responses import NotFoundError
from app.schemas.dto import SkinDTO
from app.schemas.enums import WhereConditionEnum
from app.schemas import (
     SkinHistoryTimePartModel, 
     SkinsPage, 
     PaginateSkinsMetasModel, 
     SkinWithoutMetasModel
)




class SkinService(BaseSkinService):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
          
          
     async def get_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          skin_name: str
     ) -> SkinDTO | BaseResponse:
          async with uow:
               async with cache:
                    result = await uow.skin_repo.read(
                         cache=cache,
                         cache_key=f"skin:{skin_name}",
                         where={"default": [self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ)]}
                    )
          if result is None:
               return NotFoundError
          return result
     
     
     async def search_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          paginate_data: PaginateSkinsMetasModel
     ) -> SkinsPage[SkinDTO | SkinWithoutMetasModel]:
          async with uow:
               async with cache:
                    skins, skins_count = await uow.skin_repo.read_many(
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix="search_skins"),
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         where={"default": paginate_data.generate_conditions(condition=self.condition)},
                         columns=["market_hash_name", "color", "image"] if paginate_data.metas is False else [],
                         order_by={"default": paginate_data.order_by.value},
                         order_by_mode=paginate_data.order_by_mode.value,
                         count=True
                    )
                    if paginate_data.metas is False:
                         if skins:
                              skins = [
                                   SkinWithoutMetasModel(*skin) for skin in skins
                              ]
          return SkinsPage(
               pages=skins_count,
               current_page=paginate_data.offset,
               skins=skins,
               skins_on_page=paginate_data.limit
          ).serialize()

          
     async def skin_price_history(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          skin_name: str
     ) -> SkinHistoryTimePartModel | BaseResponse:
          async with uow:
               async with cache:
                    result = await uow.skin_price_history_repo.price_by_timestamp(
                         cache=cache,
                         cache_key=f"skin_price_history:{skin_name}",
                         timestamps=[
                              (timedelta(), "all"),
                              (timedelta(days=365), "year"),
                              (timedelta(days=30), "month"),
                              (timedelta(days=7), "week"),
                              (timedelta(days=1), "day")
                         ],
                         skin_name=skin_name
                    )
          if not result:
               return NotFoundError
          return SkinHistoryTimePartModel(**result)