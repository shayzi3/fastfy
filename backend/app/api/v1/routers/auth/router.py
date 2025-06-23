from typing import Annotated
from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import (
     RedirectResponse, 
     JSONResponse, 
     HTMLResponse,
)
from fastapi.templating import Jinja2Templates

from app.core.slow_api import limiter
from app.types import TokenData
from app.responses import isresponse, ResponseSuccess
from app.core.security import jwt_encode
from app.schemas import EndpointResponse
from .service import get_auth_service, AuthService
from .schema import TelegramData
from ..dependency import current_user



auth_router = APIRouter(
     prefix="/api/v1",
     tags=["Auth"]
)
template = Jinja2Templates(
     directory="app/templates"
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
     response: Response,
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> HTMLResponse:
     result = await service.steam_processing(request.query_params)
     if isresponse(result):
          return result.response()
     
     response.set_cookie(
          key="token",
          value=await jwt_encode({"uuid": result.uuid})
     )
     return template.TemplateResponse(
          name="profile.html",
          context={
               "request": request,
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
) -> EndpointResponse[str]:
     deeplink = await service.telegram_login(user_uuid=current_user.uuid)
     return ResponseSuccess(deeplink)
     
     
     
@auth_router.post(path="/auth/TelegramProcessing")
async def telegram_processing(
     processid: str,
     data: TelegramData,
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> EndpointResponse[str]:
     result = await service.telegram_processing(
          processid=processid,
          telegram_id=data.telegram_id,
          telegram_username=data.telegram_username
     )
     return result.response()