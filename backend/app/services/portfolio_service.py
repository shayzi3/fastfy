import uuid

from typing import Type

from app.responses.abc import BaseResponse
from app.schemas import SkinsPage, JWTTokenPayloadModel, PaginateSkinsModel, PatchPortfolioSkinModel
from app.schemas.dto import UserPortfolioDTO
from app.schemas.enums import WhereConditionEnum
from app.responses import (
    CreateSuccess,
    DeleteSuccess,
    DataAlreadyExistsError,
    DataNotExistsError
)
from app.repositories.abc_condition import BaseWhereCondition
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from .abc.abc_portfolio_service import BasePortfolioService



class PortfolioService(BasePortfolioService):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
     
     
     async def get_skins_portfolio(
          self, 
          uow: BaseUnitOfWork, 
          cache: Cache, 
          token_payload: JWTTokenPayloadModel, 
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[UserPortfolioDTO]:
          async with uow:
               async with cache:
                    skins, skins_count = await uow.user_portfolio_repo.read_many(
                         cache=cache,
                         cache_key=paginate_data.cache_key(prefix=f"user_portfolio:{token_payload.uuid}"),
                         relationship_columns=["skin"],
                         limit=paginate_data.limit,
                         offset=paginate_data.offset,
                         where={
                              "default": [self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)],
                              "skin": paginate_data.generate_conditions(condition=self.condition)
                         },
                         order_by={"skin": paginate_data.order_by.value} ,
                         order_by_mode=paginate_data.order_by_mode.value,
                         count=True
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
                         where={
                              "default": [
                                   self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ),
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)
                              ]
                         }
                    )
                    if skin is None:
                         await uow.user_portfolio_repo.create(
                              cache=cache,
                              cache_keys=[f"user_portfolio:{token_payload.uuid}"],
                              values={
                                   "uuid": uuid.uuid4(),
                                   "user_uuid": token_payload.uuid,
                                   "market_hash_name": skin_name
                              }
                         )
                         await uow.commit()
                         return CreateSuccess
                    return DataAlreadyExistsError
          
          
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
                         cache_keys=[f"user_portfolio:{token_payload.uuid}"],
                         returning="market_hash_name",
                         where={
                              "default": [
                                   self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ),
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ)
                              ]
                         }
                    )
                    await uow.commit()
          if skin_deleted:
               return DeleteSuccess
          return DataNotExistsError
     
     
     async def update_skin_portfolio(
          self, 
          uow: BaseUnitOfWork, 
          cache: Cache, 
          token_payload: JWTTokenPayloadModel, 
          data: PatchPortfolioSkinModel, 
          skin_name: str
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin_updated = await uow.user_portfolio_repo.update(
                         values=data.get_update_field_values(),
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("market_hash_name", skin_name, WhereConditionEnum.EQ)
                              ]
                         },
                         cache=cache,
                         cache_keys=[f"user_portfolio:{token_payload.uuid}"],
                         returning="market_hash_name"
                    )
                    await uow.commit()
          if skin_updated:
               return DeleteSuccess
          return DataNotExistsError