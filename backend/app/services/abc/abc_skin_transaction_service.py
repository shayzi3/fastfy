from typing import Protocol

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.schemas.dto import PortfolioSkinTransactionDTO
from app.responses.abc import BaseResponse
from app.schemas import (
     JWTTokenPayloadModel, 
     CreateSkinTransactionModel, 
     UpdateSkinTransactionModel
)




class BaseSkinTransactionService(Protocol):
     
     async def get_skin_transactions(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str
     ) -> list[PortfolioSkinTransactionDTO]:
          ...
          
          
     async def create_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_data: CreateSkinTransactionModel
     ) -> BaseResponse:
          ...
          
          
     async def delete_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_uuid: str
     ) -> BaseResponse:
          ...
          
          
     async def update_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_uuid: str,
          transaction_data: UpdateSkinTransactionModel
     ) -> BaseResponse:
          ...