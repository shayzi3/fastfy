from typing import Any, Protocol
from datetime import timedelta

from app.schemas import JWTTokenPayloadModel
from app.responses.abc import BaseResponse




class BaseJWTSecurity(Protocol):
     
     async def encode(
          self, 
          data: dict[str, Any], 
          expire: timedelta = timedelta(days=20)
     ) -> str:
          ...
          
     
     async def decode(
          self,
          encode_token: str
     ) -> JWTTokenPayloadModel | BaseResponse:
          ...
          
          
     async def verify(
          self,
          encode_token: str
     ) -> BaseResponse | None:
          ...
          
     