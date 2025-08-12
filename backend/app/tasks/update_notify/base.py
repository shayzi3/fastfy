import asyncio
import uuid

from datetime import datetime

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



class UpdateNotifyBase:
     def __init__(self):
          self.steam_http_client = HttpSteamClient()
     
     
     async def _process(self, mode: UpdateMode) -> None:
          async with session_asynccontext() as async_session:
               skins = await SkinPriceInfoRepository.read_all(
                    session=async_session,
                    update_mode=mode
               )
               if skins:
                    await asyncio.gather(*[self._skin_process(skin) for skin in skins])
                    
                    
     async def _skin_process(self, skin: SkinPriceInfoModel) -> None:
          new_skin_price = await self.steam_http_client.get_skin_price(
               skin_name=skin.skin_name
          )
          if isresponse(new_skin_price):
               return
          
          time_update = datetime.now()
          update_mode = UpdateMode.filter_mode(
               volume=new_skin_price.volume,
               last_price=skin.price,
               new_price=new_skin_price
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
               
          await self._notify_process(
               skin_name=skin.skin_name,
               new_skin_price=new_skin_price.price,
               time_update=time_update.strftime("%Y-%m-%d %H:%M:%S"),
               last_skin_price=skin.price,
               last_update=skin.last_update.strftime("%Y-%m-%d %H:%M:%S")
          )
          
          
     async def _notify_process(
          self,
          skin_name: str,
          new_skin_price: float,
          time_update: str,
          last_skin_price: float | None,
          last_update: str
     ) -> None:
          async with session_asynccontext() as async_session:
               users_skins = await UserSkinRepository.read_all(
                    session=async_session,
                    selectload=True,
                    skin_name=skin_name
               )
               if users_skins and last_skin_price is not None:
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
          
          if user_skin.user.skin_percent >= skin_change_percent:
               async with session_asynccontext() as async_session:
                    await UserNotifyRepository.create(
                         session=async_session,
                         data=[
                              {
                                   "uuid": uuid.uuid4(),
                                   "user_uuid": user_skin.user.uuid,
                                   "text": (
                                        f"С {last_update} и до {time_update} цена на предмет {skin_name} "
                                        f"{price_mode} на {skin_change_percent}%"
                                   ),
                                   "notify_type": NotifyType.SKIN
                              }
                         ]
                    )
          
          
          
          
          