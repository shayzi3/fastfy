from fastapi import APIRouter



user_router = APIRouter(
     prefix="/api/v1",
     tags=["User"]
)