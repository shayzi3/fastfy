import asyncio
import uuid

from datetime import datetime

from aiogram.utils.markdown import bold, code

from app.schemas.enums import UpdateMode, NotifyType
from app.schemas import SkinPriceInfoModel, UserSkinRelModel
from app.db.session import session_asynccontext
from app.infrastracture.https.steam import HttpSteamClient
from app.db.repository import (
     SkinPriceInfoRepository, 
     SkinPriceHistoryRepository,
     UserNotifyRepository,
     UserSkinRepository
)
from app.responses import isresponse
from backend.app.utils.logger import logger



class UpdateNotifyBase:
     def __init__(self):
          self.steam_http_client = HttpSteamClient()
     
     
     async def _process(self, mode: str) -> None:
          logger.task_update_notify.info(f"START PROCESS. MODE: {mode}")
          
          async with session_asynccontext() as async_session:
               skins = await SkinPriceInfoRepository.read_all(
                    session=async_session,
                    update_mode=mode
               )
               if skins:
                    await asyncio.gather(*[self._skin_process(skin) for skin in skins])
                    
                    
     async def _skin_process(self, skin: SkinPriceInfoModel) -> None:
          logger.task_update_notify.info(f"SAVE PRICE FOR SKIN {skin.skin_name} START")
          
          try:
               new_skin_price = await self.steam_http_client.get_skin_price(
                    skin_name=skin.skin_name
               )
               if isresponse(new_skin_price):
                    return logger.task_update_notify.info(f"ERROR GET PRICE FOR SKIN {skin.skin_name}")
               
               time_update = datetime.now()
               update_mode = UpdateMode.filter_mode(
                    volume=new_skin_price.volume,
                    last_price=skin.price,
                    new_price=new_skin_price.price
               )
               
               async with session_asynccontext() as async_session:
                    await SkinPriceInfoRepository.update(
                         session=async_session,
                         where={"skin_name": skin.skin_name},
                         price=new_skin_price.price,
                         last_update=time_update,
                         update_mode=update_mode
                    )
                    await SkinPriceHistoryRepository.create(
                         session=async_session,
                         data=[
                              {
                                   "uuid": uuid.uuid4(),
                                   "skin_name": skin.skin_name,
                                   "price": new_skin_price.price,
                                   "volume": new_skin_price.volume,
                                   "timestamp": time_update
                              }
                         ]
                    )
                    logger.task_update_notify.info(f"SAVE PRICE FOR SKIN {skin.skin_name} SUCCESS")
          except Exception as ex:
               logger.task_update_notify.error(f"{ex}")
               
          await self._notify_process(
               skin_name=skin.skin_name,
               new_skin_price=new_skin_price.price,
               time_update=time_update.strftime("%d %B %H:%M:%S %Y"),
               last_skin_price=skin.price,
               last_update=skin.last_update.strftime("%d %B %H:%M:%S %Y")
          )
          
          
     async def _notify_process(
          self,
          skin_name: str,
          new_skin_price: float,
          time_update: str,
          last_skin_price: float | None,
          last_update: str
     ) -> None:
          logger.task_update_notify.info(
               f"NOTIFY FOR SKIN {skin_name} START: {last_skin_price is not None}"
          )
          
          if last_skin_price is not None:
               async with session_asynccontext() as async_session:
                    users_skins = await UserSkinRepository.read_all(
                         session=async_session,
                         selectload=True,
                         skin_name=skin_name
                    )
                    if users_skins:
                         await asyncio.gather(
                              *[
                                   self._user_notify_process(
                                        user_skin=user_skin,
                                        skin_name=skin_name,
                                        new_skin_price=new_skin_price,
                                        time_update=time_update,
                                        last_skin_price=last_skin_price,
                                        last_update=last_update
                                   ) for user_skin in users_skins
                              ]
                         )
                    
                    
     async def _user_notify_process(
          self,
          user_skin: UserSkinRelModel,
          skin_name: str,
          new_skin_price: float,
          time_update: str,
          last_skin_price: float,
          last_update: str
     ) -> None:
          skin_change_percent = ((new_skin_price - last_skin_price) / last_skin_price) * 100
          price_mode = "поднялась" if skin_change_percent > 0 else "опустилась"
          
          if (
               (skin_change_percent >= user_skin.user.skin_percent) 
               or
               (skin_change_percent*-1 >= user_skin.user.skin_percent)
          ):
               async with session_asynccontext() as async_session:
                    await UserNotifyRepository.create(
                         session=async_session,
                         data=[
                              {
                                   "uuid": uuid.uuid4(),
                                   "user_uuid": user_skin.user.uuid,
                                   "text": (
                                        f"Цена на предмет {bold(skin_name)} {code(price_mode)}\n\n"
                                        f"Прошлая цена:\n"
                                        f"Дата: {code(last_update)}\n"
                                        f"Цена: {bold(str(last_skin_price) + 'р')}\n\n"
                                        f"Новая цена:\n"
                                        f"Дата: {code(time_update)}\n"
                                        f"Цена: {bold(str(new_skin_price) + 'р')}\n\n"
                                        f"Цена предмета изменилась на {code(str(round(skin_change_percent, 2)) + '%')}"
                                   ),
                                   "notify_type": NotifyType.SKIN
                              }
                         ]
                    )
               logger.task_update_notify.info(
                    f"NEW NOTIFY WITH SKIN {skin_name} FOR USER {user_skin.user.uuid} {user_skin.user.telegram_username}"
               )
          
          
          
          
          