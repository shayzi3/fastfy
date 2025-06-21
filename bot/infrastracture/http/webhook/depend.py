from fastapi import Request, HTTPException

from core import my_config



async def validate_secret_token(request: Request) -> None:
     secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
     if secret_token != my_config.secret_token:
          raise HTTPException(
               status_code=401,
               detail="InvalidToken"
          )