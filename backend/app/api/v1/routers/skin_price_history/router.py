from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.v1.routers.dependency import current_user

from app.responses import ArgumentError
from .service import SkinPriceHistoryService, get_price_history_service


skin_history_router = APIRouter(
     prefix="/api/v1/skin",
     tags=["Skin Price History"],
     dependencies=[Depends(current_user)]
)



@skin_history_router.get("/history")
async def skin_history(
     service: Annotated[SkinPriceHistoryService, Depends(get_price_history_service)],
     skin_id: str | None = None,
     skin_name: str | None = None
):
     if (skin_id is None) and (skin_name is None):
          return ArgumentError.response()
          
     result = await service.history(
          skin_id=skin_id,
          skin_name=skin_name
     )
     return result
     
     