from typing import Any, Protocol
from datetime import timedelta

from app.schemas import JWTTokenPayloadModel




class BaseJWTSecurity(Protocol):
     
     async def encode(
          self, 
          data: dict[str, Any], 
          expire: timedelta | None = None
     ) -> str:
          ...
          
     
     async def decode(
          self,
          encode_token: str
     ) -> JWTTokenPayloadModel:
          ...