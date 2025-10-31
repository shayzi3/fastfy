from datetime import timedelta

from app.services.abc.abc_skin_service import BaseSkinService
from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from backend.app.responses.abc import BaseResponse
from app.responses import SkinNotFoundError
from app.schemas.dto import SkinDTO
from app.schemas import (
     SkinHistoryTimePartModel, 
     SkinsPage, 
     PaginateSkinsModel, 
     SkinWithoutMetasModel
)




class SkinService(BaseSkinService):
          
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
                         where={"market_hash_name": skin_name}
                    )
          if result is None:
               return SkinNotFoundError
          return result
     
     
     async def search_skin(
          self,
          cache: Cache,
          uow: BaseUnitOfWork,
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[SkinDTO | SkinWithoutMetasModel]:
          skins, skins_count = await uow.skin_repo.paginate(
               limit=paginate_data.limit,
               offset=paginate_data.offset,
               query=paginate_data.query,
               cache=cache,
               cache_key=paginate_data.cache_key(),
               order_by=paginate_data.order_by,
               order_by_mode=paginate_data.order_by_mode,
               columns=["market_hash_name", "color", "image_link"] if paginate_data.metas is False else [],
               where=paginate_data.non_nullable(
                    exclude=[
                         "limit",
                         "offset",
                         "query",
                         "order_by",
                         "order_by_mode",
                         "metas"
                    ]
               )
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
               return SkinNotFoundError
          return SkinHistoryTimePartModel(**result)