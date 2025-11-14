from typing import Annotated

from fastapi import APIRouter, Form
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.services.abc import BaseUserLikeSkinsService
from app.repositories.abc_uow import BaseUnitOfWork
from app.infrastracture.cache.abc import Cache
from app.schemas import SkinsPage, PaginateSkinsModel, JWTTokenPayloadModel
from app.schemas.presentation.dto import UserLikeSkinDTOPresentation
from app.responses import (
     isresponse,
     JWTTokenExpireError,
     JWTTokenInvalidError,
     ServerError,
     router_responses,
     CreateSuccess,
     DataAlreadyExistsError,
     DeleteSuccess,
     DataNotExistsError
)


user_likes_skins_router = APIRouter(
     prefix="/api/v1",
     tags=["Likes Skins"],
     route_class=DishkaRoute
)


@user_likes_skins_router.get(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenExpireError
     ),
     response_model=SkinsPage[UserLikeSkinDTOPresentation],
     summary="Получить все любимые скины."
)
async def get_likes_skins(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[JWTTokenPayloadModel],
     paginate_data: Annotated[PaginateSkinsModel, Form()]
):
     return await service.get_likes_skins(
          uow=uow,
          cache=cache,
          token_payload=token_payload,
          paginate_data=paginate_data
     )
     
     
@user_likes_skins_router.post(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          DataAlreadyExistsError,
          CreateSuccess
     ),
     summary="Сделать скин любимым."
)
async def create_like_skin(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[JWTTokenPayloadModel],
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


@user_likes_skins_router.delete(
     path="/likes",
     responses=router_responses(
          ServerError,
          JWTTokenExpireError,
          JWTTokenInvalidError,
          DeleteSuccess,
          DataNotExistsError
     ),
     summary="Удалить скин из любимых."
)
async def delete_like_skin(
     uow: FromDishka[BaseUnitOfWork],
     cache: FromDishka[Cache],
     service: FromDishka[BaseUserLikeSkinsService],
     token_payload: FromDishka[JWTTokenPayloadModel],
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