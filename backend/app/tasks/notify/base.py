import asyncio
import uuid
import json

from app.db.models.models import Users
from app.db.repository import (
     UserPortfolioRepository,
     SkinPriceHistoryRepository,
     NotifyRepository
)
from app.infrastracture.redis import RedisPool
from app.db.session import Session

from .schema import NotifyData



class BaseNotifyTask:
     def __init__(self):
          self.portfolio_repository = UserPortfolioRepository
          self.skin_history_repository = SkinPriceHistoryRepository
          self.notify_repository = NotifyRepository
          
     
     async def explore_skins(self, mode: str) -> None:
          all_skin_at_users = await self.portfolio_repository.read_all_task()
          if not all_skin_at_users:
               return
          
          sort_users_by_skins: dict[str, list[Users]] = {}
          for skin in all_skin_at_users:
               if skin.skin_name not in sort_users_by_skins:
                    sort_users_by_skins[skin.skin_name] = []
               sort_users_by_skins[skin.skin_name].append(skin.user)
               
          gather_funcs = []
          for skin_name, users in sort_users_by_skins.items():
               gather_funcs.append(self._explore_skin_price(skin_name, users, mode))
          await asyncio.gather(*gather_funcs)
          
          
     async def _explore_skin_price(
          self,
          skin_name: str,
          users_at_skin: list[Users],
          mode: str
     ) -> None:
          history = await self.skin_history_repository.filter_timestamp_task(
               skin_name=skin_name,
               time_mode=mode
          )
          
          notify = None
          if history and len(history) >= 2:
               month_percent = round(((history[-1]["price"] - history[0]["price"]) / history[0]["price"]) * 100, 2)
               notify = NotifyData(
                    skin_name=skin_name,
                    percent=month_percent,
                    old_time=history[0]["timestamp"],
                    new_time=history[-1]["timestamp"]
               )
          await self._send_notify(notify, users_at_skin)
               
               
     async def _send_notify(
          self,
          notify: NotifyData | None,
          users_at_skin: list[Users]
     ) -> None:
          if notify is None:
               return
          
          async with Session.session() as async_session:
               pool = RedisPool()
               for user in users_at_skin:
                    if notify.percent_valide >= user.skin_percent:
                         if user.telegram_id is not None:
                              await pool.rpush(
                                   name="telegram_notify",
                                   *(
                                        json.dumps(
                                             {
                                                  "id": user.telegram_id,
                                                  **notify.model_dump()
                                             }
                                        )
                                   )
                              )
                         await self.notify_repository.create(
                              session=async_session,
                              redis_session=pool,
                              delete_redis_values=[f"notify_history:{user.uuid}"],
                              data={
                                   "notify_id": uuid.uuid4(),
                                   "user_uuid": user.uuid,
                                   "text": f"С {notify.old_time} до {notify.new_time} цена скина {notify.skin_name} изменилась на {notify.percent}"
                              }
                         )
               await pool.close()
          
          
               
          
          

                    