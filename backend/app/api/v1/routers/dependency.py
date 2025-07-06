from fastapi import Request

from app.core.security import jwt_decode
from app.responses import TokenError, isresponse
from app.responses.abstract import AbstractResponse
from app.schemas import TokenPayload
from app.infrastracture.redis import RedisPool
from app.db.session import Session



async def current_user(
     request: Request
) -> AbstractResponse | TokenPayload:
     token = request.cookies.get("token")
     if token is not None:
          payload = await jwt_decode(token)
          if isresponse(payload):
               raise payload.exec()
          return payload
     raise TokenError.exec()