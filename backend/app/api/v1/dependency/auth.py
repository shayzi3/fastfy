from fastapi import Request
from dishka.integrations.fastapi import inject, FromDishka

from app.core.security.abc import BaseJWTSecurity
from app.responses import isresponse, JWTTokenInvalidError




class AuthDepend:
     
     @inject
     async def __call__(self, jwt_security: FromDishka[BaseJWTSecurity], request: Request):
          access_token = request.cookies.get("access_token", None)
          if access_token:
               verify_result = await jwt_security.verify(access_token)
               if isresponse(verify_result):
                    raise verify_result.exec()
          else:
               raise JWTTokenInvalidError.exec()
          