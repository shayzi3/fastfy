import jwt

from typing import Any
from datetime import datetime, timedelta

from app.responses.abstract import AbstractResponse
from app.responses import TokenError
from app.schemas import TokenPayload
from .config import my_config




async def jwt_encode(
     payload: dict[str, Any],
     expire: timedelta | None = None
):
     if expire is None:
          expire = timedelta(days=2)
          
     payload.update({
          "exp": datetime.utcnow() + expire,
          "iat": datetime.utcnow()
     })
     return jwt.encode(
          payload=payload,
          key=my_config.jwt_secret,
          algorithm=my_config.jwt_alghoritm
     )
     
     
     
async def jwt_decode(
     token: str
) -> AbstractResponse | TokenPayload:
     try:
          result = jwt.decode(
               jwt=token,
               key=my_config.jwt_secret,
               algorithms=[my_config.jwt_alghoritm]
          )
     except:
          return TokenError
     return TokenPayload.model_validate(result)
     
     