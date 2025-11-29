from datetime import timedelta
from typing import Type

from app.services.abc.abc_skin_service import BaseSkinService
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.responses.abc import BaseResponse
from app.repositories.abc_condition import BaseWhereCondition
from app.responses import NotFoundError
from app.schemas.dto import SkinDTO
from app.schemas.enums import WhereConditionEnum, OrderByModeEnum
from app.schemas import (
     SkinHistoryTimePartModel, 
     SkinsPage, 
     PaginateSkinsModel
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
                         joinedload_relship_columns=["collections"],
                         where={"default": [self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ)]}
                    )
          if result is None:
               return NotFoundError
          return result.as_presentation()
     
     
     async def search_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[SkinDTO]:
          async with uow:
               async with cache:
                    where_conditions = {
                         "default": paginate_data.generate_conditions(condition=self.condition),
                    }
                    if paginate_data.collection:
                         where_conditions.update(
                              {"collections": [self.condition("collection", paginate_data.collection, WhereConditionEnum.EQ)]}
                         )
                         
                    skins, skins_count = await uow.skin_repo.read_many(
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix="search_skins"),
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         relationship_columns=["collections"] if where_conditions.get("collections", None) else [],
                         joinedload_relship_columns=["collections"],
                         where=where_conditions,
                         order_by={"default": [(paginate_data.order_by, paginate_data.order_by_mode)]},
                         count=True
                    )
          return SkinsPage(
               pages=skins_count,
               current_page=paginate_data.offset,
               skins=[skin.as_presentation() for skin in skins],
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
                              (timedelta(days=100*356), "all"),
                              (timedelta(days=365), "year"),
                              (timedelta(days=30), "month"),
                              (timedelta(days=7), "week"),
                              (timedelta(days=1), "day")
                         ],
                         where={"default": [self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ)]},
                         order_by={"default": [("timestamp", OrderByModeEnum.ASC)]}
                    )
          if not result:
               return NotFoundError
          return SkinHistoryTimePartModel(**result)