from typing import Annotated
from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

from app.core.template import templates
from app.core.slow_api import limiter
from app.type import TokenData
from app.responses import isresponse
from app.core.security import jwt_encode
from .service import get_auth_service, AuthService
from .schema import TelegramData
from ..dependency import current_user



auth_router = APIRouter(
     prefix="/api/v1",
     tags=["Auth"]
)



@auth_router.get(path="/auth/SteamLogin")
async def steam_redirect(
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
     url = await service.steam_redirest()
     return RedirectResponse(url=url)
      
     
     
     
@auth_router.get(path="/auth/SteamProcessing")
async def steam_processing(
     request: Request,
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> HTMLResponse:
     result = await service.steam_processing(request.query_params)
     if isresponse(result):
          return result.response()
     
     return templates.TemplateResponse(
          name="profile.html",
          context={
               "request": request,
               "token": await jwt_encode({"uuid": result.uuid}),
               "steam_name": result.steam_name,
               "steam_avatar": result.steam_avatar
          }
     )



@auth_router.get(path="/auth/TelegramLogin")
@limiter.limit("1/4 minute")
async def telegram_login(
     request: Request,
     current_user: Annotated[TokenData, Depends(current_user)],
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> str:
     deeplink = await service.telegram_login(user_uuid=current_user.uuid)
     return Response(content=deeplink)
     
     
     
     
@auth_router.post(path="/auth/TelegramProcessing")
async def telegram_processing(
     processid: str,
     data: TelegramData,
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> JSONResponse:
     result = await service.telegram_processing(
          processid=processid,
          telegram_id=data.telegram_id,
          telegram_username=data.telegram_username
     )
     return result.response()