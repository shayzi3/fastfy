from typing import Protocol, Type

from app.repositories.abc_uow import BaseUnitOfWork
from app.repositories.abc_condition import BaseWhereCondition
from app.utils.math_operations.abc import BaseMathOperations
from app.infrastracture.cache.abc import Cache
from app.schemas.dto import SkinPortfolioTransactionDTO
from app.responses.abc import BaseResponse
from app.schemas import (
     JWTTokenPayloadModel, 
     CreateSkinTransactionModel, 
     PatchSkinTransactionModel
)




class BaseSkinTransactionService(Protocol):
     def __init__(
          self, 
          condition: Type[BaseWhereCondition],
          math_operation: BaseMathOperations
     ):
          self.condition = condition
          self.math_operation = math_operation
     
     
     async def get_skin_transactions(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str
     ) -> list[SkinPortfolioTransactionDTO] | BaseResponse:
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
          transaction_data: PatchSkinTransactionModel
     ) -> BaseResponse:
          ...
          
          
     async def _update_skin_benefit(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str
     ) -> None:
          ...