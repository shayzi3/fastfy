import uvicorn

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.routers import include_routers
from app.core.slow_api import limiter



app = FastAPI(title="FastFy")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
include_routers(app)



if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085
     )