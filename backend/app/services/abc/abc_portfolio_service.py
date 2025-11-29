from typing import Protocol

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.responses.abc import BaseResponse
from app.repositories.abc_condition import BaseWhereCondition

from app.schemas.dto import SkinPortfolioDTO
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginateSkinsModel, PatchPortfolioSkinModel



class BasePortfolioService(Protocol):
     def __init__(self, condition: BaseWhereCondition):
          self.condition = condition
          
     
     async def get_skins_portfolio(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginateSkinsModel
     ) -> SkinsPage[SkinPortfolioDTO]:
          ...
          
     async def delete_skin_portolio(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str
     ) -> BaseResponse:
          ...
          
     async def create_skin_portfolio(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          skin_name: str
     ) -> BaseResponse:
          ...
          
     async def update_skin_portfolio(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          data: PatchPortfolioSkinModel,
          skin_name: str
     ) -> BaseResponse:
          ...