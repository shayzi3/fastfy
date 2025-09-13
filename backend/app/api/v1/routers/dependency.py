from typing import Annotated
from fastapi import Depends, Request

from app.core.config import my_config
from app.infrastracture.redis import RedisPool, get_redis_session
from app.responses import AuthError, SecretTokenError
from app.responses.abstract import AbstractResponse
from app.schemas import UserModel



async def current_user_uuid(
     telegram_id: int,
     redis_session: Annotated[RedisPool, Depends(get_redis_session)]
) -> AbstractResponse | UserModel:
     user_uuid = await redis_session.get(str(telegram_id))
     if user_uuid is not None:
         return user_uuid
     raise AuthError.exec()


async def valide_secret_bot_token(request: Request) -> None:
     secret_bot_token = request.headers.get("Secret-Bot-Token")
     if secret_bot_token != my_config.secret_bot_token:
          raise SecretTokenError.exec()