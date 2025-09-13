from app.schemas import SkinPriceInfoModel
from app.db.models import SkinsPriceInfo
from .base import BaseRepository


class SkinPriceInfoRepository(
     BaseRepository[SkinPriceInfoModel, None]
):
     model = SkinsPriceInfo