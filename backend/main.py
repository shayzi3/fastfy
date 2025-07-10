import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded

from app.responses import rate_limit_exceeded
from app.api.v1.routers import include_routers
from app.core.slow_api import limiter
from app.tasks.update_prices import UpdatePricesTasks
from app.tasks.notify import NotifyTask


@asynccontextmanager
async def lifespan(_: FastAPI):
     update_prices_task = UpdatePricesTasks()
     notify_task = NotifyTask()
     
     await update_prices_task.run()
     await notify_task.run()
     
     yield
     
     

app = FastAPI(title="FastFy", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded)
include_routers(app)



if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085
     )