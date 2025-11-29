
from typing import Any
from datetime import timedelta, datetime

from jose import jwt, exceptions
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
                    token=encode_token,
                    key=my_config.jwt_secret_key,
                    algorithms=[my_config.jwt_algorithm]
               )
               return JWTTokenPayloadModel.model_validate(data)
          except exceptions.ExpiredSignatureError:
               return JWTTokenExpireError
          
          except exceptions.JWTError:
               return JWTTokenInvalidError
          
     
     async def encode(
          self, 
          data: dict[str, Any], 
          expire: timedelta = timedelta(days=20)
     ) -> str:
          payload_time = {
               "iat": datetime.now().timestamp(),
               "exp": (datetime.now() + expire).timestamp()
          }
          data.update(payload_time)
          
          return jwt.encode(
               claims=data,
               key=my_config.jwt_secret_key,
               algorithm=my_config.jwt_algorithm
          )
          
          
     async def verify(
          self, 
          encode_token: str
     ) -> BaseResponse | None:
          try:
               jwt.decode(
                    token=encode_token,
                    key=my_config.jwt_secret_key,
                    algorithms=[my_config.jwt_algorithm]
               )
          except exceptions.ExpiredSignatureError:
               return JWTTokenExpireError
          
          except exceptions.JWTError:
               return JWTTokenInvalidError