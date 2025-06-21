import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from dishka.integrations.aiogram import (
     AiogramProvider,
     setup_dishka
)
from dishka import make_async_container 

from provider import DependencyProvider
from core import my_config, bot, dp
from handlers import __routers__
from infrastracture.http.webhook import webhook_router



@asynccontextmanager
async def lifespan(_: FastAPI):
     dp.include_routers(*__routers__)
     
     container = make_async_container(DependencyProvider(), AiogramProvider())
     setup_dishka(router=dp, container=container, auto_inject=True)
     dp.shutdown.register(container.close)
     
     await bot.set_webhook(
          url=my_config.webhook_url,
          secret_token=my_config.secret_token,
          drop_pending_updates=True,
          allowed_updates=dp.resolve_used_update_types()
     )
     yield
     await bot.delete_webhook(drop_pending_updates=True)



app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router)


if __name__ == "__main__":
     uvicorn.run("main:app", port=8086, reload=True)


