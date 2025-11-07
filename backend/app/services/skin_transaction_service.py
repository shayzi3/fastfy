import uuid

from typing import Type

from app.repositories.abc_uow import BaseUnitOfWork
from app.repositories.abc_condition import BaseWhereCondition
from app.infrastracture.cache.abc import Cache
from app.schemas.dto import PortfolioSkinTransactionDTO
from app.responses.abc import BaseResponse
from app.services.abc import BaseSkinTransactionService
from app.schemas.enums import WhereConditionEnum
from app.responses import (
     ArgumentError,
     NotFoundError,
     CreateSuccess,
     UpdateError,
     UpdateSuccess,
     DeleteSuccess,
     DeleteError
)
from app.schemas import (
     JWTTokenPayloadModel, 
     CreateSkinTransactionModel, 
     PatchSkinTransactionModel
)


class SkinTransactionService(BaseSkinTransactionService):
     def __init__(self, condition: Type[BaseWhereCondition]):
          self.condition = condition
          
     
     async def get_skin_transactions(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          **kwargs
     ) -> list[PortfolioSkinTransactionDTO] | BaseResponse:
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("uuid", portfolio_skin_uuid, WhereConditionEnum.EQ)
                              ]
                         },
                    )
                    if skin_exists_at_user_portfolio:
                         skins, _ = await uow.portoflio_skin_transaction_repo.read_many(
                              where={"default": [self.condition("uuid", portfolio_skin_uuid, WhereConditionEnum.EQ)]},
                              cache=cache,
                              cache_key=f"portfolio_skin_transaction:{portfolio_skin_uuid}"
                         )
                         return skins
                    return NotFoundError
          
          
     async def create_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_data: CreateSkinTransactionModel,
          **kwargs
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("uuid", portfolio_skin_uuid, WhereConditionEnum.EQ)
                              ]
                         },
                    )
                    if skin_exists_at_user_portfolio:
                         await uow.portoflio_skin_transaction_repo.create(
                              values={
                                   "uuid": uuid.uuid4(),
                                   "portfolio_skin_uuid": portfolio_skin_uuid,
                                   **transaction_data.model_dump()
                              },
                              cache=cache,
                              cache_keys=[f"portfolio_skin_transaction:{portfolio_skin_uuid}"]
                         )
                         await uow.commit()
                         return CreateSuccess
                    return NotFoundError
          
          
     async def delete_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_uuid: str,
          **kwargs
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("uuid", portfolio_skin_uuid, WhereConditionEnum.EQ)
                              ]
                         },
                    )
                    if skin_exists_at_user_portfolio:
                         result = await uow.portoflio_skin_transaction_repo.delete(
                              where={"default": [self.condition("uuid", transaction_uuid, WhereConditionEnum.EQ)]},
                              cache=cache,
                              cache_keys=[f"portfolio_skin_transaction:{portfolio_skin_uuid}"],
                              returning="uuid"
                         )
                         await uow.commit()
                         if result:
                              return DeleteSuccess
                         return DeleteError
                    return NotFoundError
          
     
     async def update_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_uuid: str,
          transaction_data: PatchSkinTransactionModel,
          **kwargs
     ) -> BaseResponse:
          if not transaction_data.non_nullable():
               return ArgumentError
          
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "default": [
                                   self.condition("user_uuid", token_payload.uuid, WhereConditionEnum.EQ),
                                   self.condition("uuid", portfolio_skin_uuid, WhereConditionEnum.EQ)
                              ]
                         },
                    )
                    if skin_exists_at_user_portfolio:
                         await uow.portoflio_skin_transaction_repo.update(
                              values=transaction_data.get_update_field_values(),
                              where={"default": [self.condition("uuid", transaction_uuid, WhereConditionEnum.EQ)]},
                              cache=cache,
                              cache_keys=[f"portfolio_skin_transaction:{portfolio_skin_uuid}"]
                         )
                         await uow.commit()
                         return UpdateSuccess
                    return UpdateError