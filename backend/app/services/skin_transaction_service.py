import uuid

from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.schemas.dto import PortfolioSkinTransactionDTO
from app.responses.abc import BaseResponse
from app.services.abc import BaseSkinTransactionService
from app.responses import (
     TransactionNotFound, 
     SkinTransactionSuccess,
     SkinTransactionError,
     ArgumentError
)
from app.schemas import (
     JWTTokenPayloadModel, 
     CreateSkinTransactionModel, 
     UpdateSkinTransactionModel
)


class SkinTransactionService(BaseSkinTransactionService):
     
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
                              "user_uuid": token_payload.uuid,
                              "uuid": portfolio_skin_uuid
                         }
                    )
                    if skin_exists_at_user_portfolio:
                         skins = await uow.portoflio_skin_transaction_repo.read_all(
                              where={"porfolio_skin_uuid": portfolio_skin_uuid},
                              cache=cache,
                              cache_key=f"portfolio_skin_transaction:{portfolio_skin_uuid}"
                         )
                         return skins
                    return TransactionNotFound
          
          
     async def create_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_data: CreateSkinTransactionModel
     ) -> BaseResponse:
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "user_uuid": token_payload.uuid,
                              "uuid": portfolio_skin_uuid
                         }
                    )
                    if skin_exists_at_user_portfolio:
                         await uow.portoflio_skin_transaction_repo.create(
                              values={
                                   "uuid": uuid.uuid4(),
                                   "portfolio_skin_uuid": portfolio_skin_uuid,
                                   **transaction_data.model_dump()
                              }
                         )
                         await uow.commit()
                         return SkinTransactionSuccess
                    return SkinTransactionError
          
          
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
                              "user_uuid": token_payload.uuid,
                              "uuid": portfolio_skin_uuid
                         }
                    )
                    if skin_exists_at_user_portfolio:
                         result = await uow.portoflio_skin_transaction_repo.delete(
                              where={"uuid": transaction_uuid},
                              cache=cache,
                              cache_keys=[f"portfolio_skin_transaction:{portfolio_skin_uuid}"],
                              returning=True
                         )
                         await uow.commit()
                         if result:
                              return SkinTransactionSuccess
                         return SkinTransactionError
                    return TransactionNotFound
          
          
     async def update_skin_transaction(
          self,
          uow: BaseUnitOfWork,
          cache: Cache,
          token_payload: JWTTokenPayloadModel,
          portfolio_skin_uuid: str,
          transaction_uuid: str,
          transaction_data: UpdateSkinTransactionModel,
          **kwargs
     ) -> BaseResponse:
          if not transaction_data.non_nullable():
               return ArgumentError
          
          async with uow:
               async with cache:
                    skin_exists_at_user_portfolio = await uow.user_portfolio_repo.read(
                         where={
                              "user_uuid": token_payload.uuid,
                              "uuid": portfolio_skin_uuid
                         }
                    )
                    if skin_exists_at_user_portfolio:
                         await uow.portoflio_skin_transaction_repo.update(
                              values=transaction_data.non_nullable(),
                              where={"uuid": transaction_uuid},
                              cache=cache,
                              cache_keys=[f"portfolio_skin_transaction:{portfolio_skin_uuid}"]
                         )
                         await uow.commit()
                         return SkinTransactionSuccess
                    return SkinTransactionError