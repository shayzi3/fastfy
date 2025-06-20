from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import (
     RedirectResponse, 
     JSONResponse, 
     HTMLResponse,
)
from fastapi.templating import Jinja2Templates

from app.responses import isresponse
from app.core.security import jwt_encode
from .service import get_auth_service, AuthService



auth_router = APIRouter(
     prefix="/api/v1/auth",
     tags=["Auth"]
)
template = Jinja2Templates(
     directory="app/templates"
)



@auth_router.get(path="/steam/login")
async def steam_redirect(
     service: Annotated[AuthService, Depends(get_auth_service)]
) -> RedirectResponse:
     url = await service.steam_redirest()
     return RedirectResponse(url=url)
     
     
     
@auth_router.get(path="/steam/processing", response_class=HTMLResponse)
async def steam_processing(
     request: Request,
     service: Annotated[AuthService, Depends(get_auth_service)]
):
     result = await service.steam_processing(request.query_params)
     if isresponse(result):
          return result.response()
     
     return template.TemplateResponse(
          name="profile.html",
          context={
               "request": request,
               "token": await jwt_encode({"uuid": result.uuid}),
               "steam_name": result.steam_name,
               "steam_avatar": result.steam_avatar
          }
     )



@auth_router.get(path="/telegram/login")
async def telegram_login() -> JSONResponse:
     ...
     
     
@auth_router.get(path="/telegram/processing")
async def telegram_processing() -> JSONResponse:
     ...