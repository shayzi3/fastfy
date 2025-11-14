import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from dishka.integrations.fastapi import setup_dishka

from app.core import my_config
from app.api.v1.dependency import container
from app.api.v1 import (
     include_routers, 
     include_exception_handlers,
     include_middleware
)
# from app.tasks import (
#      run_tasks,
#      UpdateNotifyTask,
#      UpdatePriceAtDaysTask 
# )


 


@asynccontextmanager
async def lifespan(app: FastAPI):
     # await run_tasks(
     #      UpdateNotifyTask(),
     #      UpdatePriceAtDaysTask()
     # )
     # await test_connections.start()  
     yield
     await app.state.dishka_container.close()



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
     version="1.0.0",
     # lifespan=lifespan
)
include_routers(app)
include_exception_handlers(app)
include_middleware(app)
setup_dishka(container=container, app=app)



if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085,
          host=my_config.local_host
     )