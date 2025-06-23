from typing import Annotated
from fastapi import APIRouter, Depends

from app.responses import isresponse, ResponseSuccess
from app.schemas import TokenPayload, UserModel, SteamItem, EndpointResponse
from ..dependency import current_user
from .service import UserService, get_user_service


user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"]
)



@user_router.get(path="/user")
async def get_user(
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserService, Depends(get_user_service)],
     uuid: str | None = None
) -> EndpointResponse[UserModel]:
     user = current_user.uuid if uuid is None else uuid
     result = await service.get_user(uuid=user)
     if isresponse(result):
          return result.response()
     return ResponseSuccess(result)
     
     
     
@user_router.get(path="/user/SteamInventory")
async def get_steam_inventory(
     current_user: Annotated[TokenPayload, Depends(current_user)],
     service: Annotated[UserService, Depends(get_user_service)],
     uuid: str | None = None
) -> EndpointResponse[list[SteamItem]]:
     user = current_user.uuid if uuid is None else uuid
     result = await service.get_user_steam_inventory(user)
     if isresponse(result):
          return result.response()
     return ResponseSuccess(result)