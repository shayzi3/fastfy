from typing import Annotated
from fastapi import Request, Depends

from app.infrastracture.redis import RedisPool, get_redis_session
from app.core.security import jwt_decode, jwt_encode
from app.responses import isresponse
from app.core.security import jwt_decode



async def valide_token(
     redis_session: Annotated[RedisPool, Depends(get_redis_session)],
     request: Request,
     session: int | None = None
) -> tuple[str, str | None] | None:
     token = request.cookies.get("token")
     
     if token is None:
          if session is not None:
               uuid = await redis_session.get(f"session:{session}")
               if uuid is None:
                    return None
               
               await redis_session.delete(f"session:{session}")
               generate_token = await jwt_encode({"uuid": uuid})
               return (uuid, generate_token)
          return None
     else:
          payload = await jwt_decode(token)
          if isresponse(payload):
               return None
          return (payload.uuid, None)
     
     
          
          

     