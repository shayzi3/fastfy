import jwt

from typing import Any
from datetime import timedelta, datetime

from fastapi import Request

from app.schemas import JWTTokenPayloadModel
from app.core import my_config
from app.responses.abc import BaseResponse
from app.responses import JWTTokenExpireError, JWTTokenInvalidError, isresponse
from .abc import BaseJWTSecurity




class JWTSecurity(BaseJWTSecurity):
     
     
     async def __call__(self, request: Request) -> JWTTokenPayloadModel:
          jwt_token = request.cookies.get("access_token", None)
          if jwt_token is None:
               raise JWTTokenInvalidError.exec()
          
          payload = await self.decode(encode_token=jwt_token)
          if isresponse(payload):
               raise payload.exec()
          return payload
     
     
     async def decode(
          self, 
          encode_token: str
     ) -> JWTTokenPayloadModel | BaseResponse:
          try:
               data = jwt.decode(
                    jwt=encode_token,
                    key=my_config.jwt_secret_key,
                    algorithms=[my_config.jwt_algorithm]
               )
               return JWTTokenPayloadModel.model_validate(data)
          except jwt.ExpiredSignatureError:
               return JWTTokenExpireError
          
          except jwt.InvalidTokenError:
               return JWTTokenInvalidError
          
          
     async def encode(
          self, 
          data: dict[str, Any], 
          expire: timedelta = timedelta(days=20)
     ) -> str:
          payload_time = {
               "iat": datetime.now(),
               "exp": datetime.now() + expire
          }
          data.update(payload_time)
          
          return jwt.encode(
               payload=data,
               key=my_config.jwt_secret_key,
               algorithm=my_config.jwt_algorithm
          )