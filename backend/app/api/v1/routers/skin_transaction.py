from typing import Annotated

from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.infrastracture.cache.abc import Cache
from app.repositories.abc_uow import BaseUnitOfWork
from app.services.abc import BaseSkinTransactionService
from app.core.security.abc import BaseJWTSecurity
from app.schemas.dto import UserLikeSkinDTO
from app.schemas import CreateSkinTransactionModel, PatchSkinTransactionModel
from app.responses import (
     isresponse,
     router_responses,
     ServerError,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     NotFoundError,
     CreateSuccess,
     UpdateError,
     UpdateSuccess,
     DeleteError,
     DeleteSuccess,
     ArgumentError
)


skin_transaction_router = APIRouter(
     prefix="/api/v1",
     tags=["Transactions"],
     route_class=DishkaRoute
)


@skin_transaction_router.get(
     path="/transaction",
     response_model=list[UserLikeSkinDTO],
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          NotFoundError
     )
)
async def get_skin_transactions(
     service: FromDishka[BaseSkinTransactionService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     token_payload: FromDishka[BaseJWTSecurity],
     portfolio_skin_uuid: str
):
     result = await service.get_skin_transactions(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          portfolio_skin_uuid=portfolio_skin_uuid
     )
     if isresponse(result):
          return result.response()
     return result



@skin_transaction_router.post(
     path="/transaction",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          CreateSuccess,
          NotFoundError
     )
)
async def create_skin_transaction(
     service: FromDishka[BaseSkinTransactionService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     token_payload: FromDishka[BaseJWTSecurity],
     portfolio_skin_uuid: str,
     transaction_data: CreateSkinTransactionModel
):
     result = await service.create_skin_transaction(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          portfolio_skin_uuid=portfolio_skin_uuid,
          transaction_data=transaction_data
     )
     return result.response()


@skin_transaction_router.patch(
     path="/transaction",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          UpdateSuccess,
          UpdateError,
          ArgumentError
     )
)
async def update_skin_transaction(
     service: FromDishka[BaseSkinTransactionService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     token_payload: FromDishka[BaseJWTSecurity],
     portfolio_skin_uuid: str,
     transaction_uuid: str,
     transaction_data: Annotated[PatchSkinTransactionModel, Form()]
):
     result = await service.update_skin_transaction(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          portfolio_skin_uuid=portfolio_skin_uuid,
          transaction_uuid=transaction_uuid,
          transaction_data=transaction_data
     )
     return result.response()


@skin_transaction_router.delete(
     path="/transaction",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          DeleteSuccess,
          DeleteError,
          NotFoundError
     )
)
async def delete_skin_transaction(
     service: FromDishka[BaseSkinTransactionService],
     cache: FromDishka[Cache],
     uow: FromDishka[BaseUnitOfWork],
     token_payload: FromDishka[BaseJWTSecurity],
     portfolio_skin_uuid: str,
     transaction_uuid: str,
):
     result = await service.delete_skin_transaction(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          portfolio_skin_uuid=portfolio_skin_uuid,
          transaction_uuid=transaction_uuid
     )
     return result.response()