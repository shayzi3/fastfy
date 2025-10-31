from typing import Annotated

from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka

from app.services.abc import BaseUserLikeSkinsService
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.core.security.abc import BaseJWTSecurity
from app.schemas import SkinsPage, PaginateUserLikeSkinsModel
from app.schemas.dto import UserLikeSkinDTO
from app.responses import (
     isresponse,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     ServerError,
     SkinCreateSuccess,
     SkinAlreadyExistsError,
     SkinDeleteSuccess,
     SkinNotExistsError,
     router_responses
)


user_likes_skins = APIRouter(
     prefix="/api/v1/user",
     tags=["User Likes"]
)


@user_likes_skins.get(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenExpireError
     ),
     response_model=SkinsPage[UserLikeSkinDTO],
     summary="Получить все любимые скины."
)
async def get_likes_skins(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[BaseJWTSecurity],
     paginate_data: Annotated[PaginateUserLikeSkinsModel, Form()]
):
     return await service.get_likes_skins(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          paginate_data=paginate_data
     )
     
     
@user_likes_skins.post(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          SkinAlreadyExistsError,
          SkinCreateSuccess
     ),
     summary="Сделать скин любимым."
)
async def create_like_skin(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[BaseJWTSecurity],
     skin_name: str
):
     result = await service.create_like_skin(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result


@user_likes_skins.delete(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          SkinDeleteSuccess,
          SkinNotExistsError
     ),
     summary="Удалить скин из любимых."
)
async def delete_like_skin(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[BaseJWTSecurity],
     skin_name: str
):
     result = await service.delete_like_skin(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          skin_name=skin_name
     )
     if isresponse(result):
          return result.response()
     return result