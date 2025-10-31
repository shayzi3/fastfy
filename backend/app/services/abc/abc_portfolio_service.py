from typing import Protocol

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.responses.abc import BaseResponse

from app.schemas.dto import UserPortfolioDTO
from app.schemas import JWTTokenPayloadModel, SkinsPage, PaginatePortfolioSkinsModel



class BasePortfolioService(Protocol):
          
     
     async def get_skins_portfolio(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          paginate_data: PaginatePortfolioSkinsModel
     ) -> SkinsPage[UserPortfolioDTO]:
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