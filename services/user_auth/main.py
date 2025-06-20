import uvicorn

from fastapi import FastAPI

from app.api.v1.routers import auth_router


app = FastAPI(title="FastFy")
app.include_router(auth_router)


if __name__ == "__main__":
     uvicorn.run(
          app="main:app",
          reload=True,
          port=8085
     )