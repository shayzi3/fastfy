import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.routers import include_routers



@asynccontextmanager
async def lifespan(_: FastAPI):
     ...
     


app = FastAPI(title="FastFy")
include_routers(app)



if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085
     )