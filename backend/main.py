import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routers import include_routers
from app.tasks import (
     run_tasks,
     UpdateNotifyTask,
     UpdatePriceAtDaysTask
)



@asynccontextmanager
async def lifespan(_: FastAPI):
     await run_tasks(
          UpdateNotifyTask(),
          UpdatePriceAtDaysTask()
     )
     


app = FastAPI(
     title="FastFy",
     summary=(
          "Ознакомление с терминами: "
          "1. Процент: цифра от 0 до 100. "
          "Нужно для того, чтобы фиксировать изменение стоимости скинов. "
          "2. Текущий аккаунт: один телеграм аккаунт может быть привязан "
          "к разным steam_id. Текущий аккаунт показывает к какому аккаунту "
          "привязан отправленный telegram_id. По ключу telegram_id в Redis "
          "хранится uuid."
     ),
     version="1.0.0"
)
include_routers(app)



if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085
     )