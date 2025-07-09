import asyncio
import uuid

from app.db.models.models import Skins
from app.db.repository import SkinRepository, SkinPriceHistoryRepository
from app.db.session import Session
from app.infrastracture.redis import RedisPool
from app.schemas.enums import UpdateMode
from app.infrastracture.https.steam import HttpSteamClient
from app.responses import isresponse



class BaseUpdatePricesTasks:
     def __init__(self):
          self.steam_client = HttpSteamClient()
          self.skin_repository = SkinRepository
          self.skin_history_repository = SkinPriceHistoryRepository


     async def _update_skin(
          self,
          skin: Skins, 
          timer: int = 0
     ) -> None:
          await asyncio.sleep(timer)
          result = await self.steam_client.get_skin_price(skin_name=skin.name)
          if isresponse(result):
               await self._update_skin(skin, timer + 2)
          
          price, volume = result
          await self._update_skin_in_database(
               skin=skin,
               price=price,
               volume=volume
          )
          
          
     async def _update_skin_in_database(
          self, 
          skin: Skins, 
          price: float,
          volume: int
     ) -> None:
          async with Session.session() as async_session:
               mode = UpdateMode.filter_mode(volume)
               pool = RedisPool()
               await self.skin_repository.update(
                    session=async_session,
                    redis_session=pool,
                    delete_redis_values=[f"skin:{skin.name}"],
                    where={"name": skin.name},
                    price=price,
                    update_mode=mode
               )
               await self.skin_history_repository.create(
                    session=async_session,
                    redis_session=pool,
                    delete_redis_values=[f"skin_price_history:{skin.name}"],
                    data={
                         "item_id": uuid.uuid4(),
                         "skin_name": skin.name,
                         "price": price,
                         "volume": volume
                    }
               )
               await pool.close()
          
          
     async def update_all_skins(
          self, 
          mode: UpdateMode
     ) -> None:
          gather_funcs = []
          skins = await self.skin_repository.read_all_task(mode)
          for skin in skins:
               gather_funcs.append(self._update_skin(skin))
          await asyncio.gather(*gather_funcs)