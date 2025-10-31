import uuid

from backend.app.responses.abc import BaseResponse
from app.schemas import SkinsPage, JWTTokenPayloadModel, PaginatePortfolioSkinsModel
from app.schemas.dto import UserPortfolioDTO
from app.responses import (
     SkinCreateSuccess, 
     SkinAlreadyExistsError,
     SkinNotExistsError,
     SkinDeleteSuccess,
)
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from .abc.abc_portfolio_service import BasePortfolioService



class PortfolioService(BasePortfolioService):
     
     async def get_skins_portfolio(
          self, 
          uow: BaseUnitOfWork, 
          cache: Cache, 
          token_payload: JWTTokenPayloadModel, 
          paginate_data: PaginatePortfolioSkinsModel
     ) -> SkinsPage[UserPortfolioDTO]:
          async with uow:
               async with cache:
                    skins, skins_count = await uow.user_portfolio_repo.paginate(
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         where={"user_uuid": token_payload.uuid},
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix=f"user_portfolio-{token_payload.uuid}"),
                    )
          return SkinsPage(
               pages=skins_count,
               current_page=paginate_data.offset,
               skins=skins,
               skins_on_page=paginate_data.limit
          ).serialize()
          
          
     async def create_skin_portfolio(
          self, 
          uow: BaseUnitOfWork, 
          cache: Cache,
          token_payload: JWTTokenPayloadModel, 
          skin_name: str
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin = await uow.user_portfolio_repo.read(
                         where={"market_hash_name": skin_name}
                    )
                    if skin is None:
                         await uow.user_portfolio_repo.create(
                              cache=cache,
                              cache_keys=[f"user_portfolio-{token_payload.uuid}"],
                              values={
                                   "uuid": uuid.uuid4(),
                                   "user_uuid": token_payload.uuid,
                                   "market_hash_name": skin_name
                              }
                         )
                         await uow.commit()
                         return SkinCreateSuccess
                    return SkinAlreadyExistsError
          
          
     async def delete_skin_portolio(
          self, 
          uow: BaseUnitOfWork, 
          cache: Cache, 
          token_payload: JWTTokenPayloadModel, 
          skin_name: str
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin_deleted = await uow.user_portfolio_repo.delete(
                         cache=cache,
                         cache_keys=[f"user_portfolio-{token_payload.uuid}"],
                         returning=True,
                         where={"market_hash_name": skin_name, "user_uuid": token_payload.uuid}
                    )
                    await uow.commit()
                    
          if skin_deleted:
               return SkinDeleteSuccess
          return SkinNotExistsError
                    