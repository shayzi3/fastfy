from fastapi import APIRouter, Request, Depends, Response
from aiogram.types import Update

from core import bot, dp
from .depend import validate_secret_token


webhook_router = APIRouter(
     prefix="/webhook",
     dependencies=[Depends(validate_secret_token)],
     tags=["Webhook"]
)


@webhook_router.post("/telegram")
async def webhook_telegram(request: Request):
     update = Update.model_validate(await request.json(), context={"bot": bot})
     await dp.feed_update(bot, update)
     return Response()



     
     
