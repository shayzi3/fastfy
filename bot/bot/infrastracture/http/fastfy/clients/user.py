from bot.schemas.fastfy import (
     UserSchema,
     DetailSchema,
     SkinsOnPageSchema,
     SkinSteamInventorySchema,
     UserPortfolioSkinSchema,
     UserNotifySchema
)
from bot.logger import logger
from ..base import HttpClient



class UserClient(HttpClient):
     
     
     async def get_user(
          self,
          telegram_id: int
     ) -> DetailSchema | UserSchema:
          response = await self.request(
               method="GET",
               url=self.url_builder("/user"),
               query_arguments={"telegram_id": telegram_id}
          )
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Get user error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          return UserSchema.model_validate(response.obj)
     
     
     async def change_percent_user(
          self,
          telegram_id: int,
          percent: int
     ) -> DetailSchema:
          response = await self.request(
               method="PATCH",
               url=self.url_builder("/user"),
               query_arguments={
                    "telegram_id": telegram_id,
                    "skin_percent": percent
               }
          )
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Change percent user error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          return DetailSchema(detail="Процент успешно обнолён.")
     
     
     async def get_steam_inventory_user(
          self,
          telegram_id: int,
          offset: int,
          limit: int
     ) -> DetailSchema | SkinsOnPageSchema[SkinSteamInventorySchema]:
          response = await self.request(
               method="GET",
               url=self.url_builder("/user/SteamInventory"),
               query_arguments={
                    "telegram_id": telegram_id,
                    "offset": offset,
                    "limit": limit
               }
          )
          if response.status_code == 400:
               return DetailSchema(detail="Скины недоступны.")
          
          elif response.status_code == 403:
               logger.fastfy_client.error(msg=f"Get steam inventory user error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Steam не вернул ваш инвентарь. Повторите запрос позднее.")
          
          elif response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Get steam inventory user error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          return SkinsOnPageSchema(
               pages=response.obj.get("pages"),
               current_page=response.obj.get("current_page"),
               skins=response.obj.get("skins"),
               skin_model=SkinSteamInventorySchema
          )
          
     async def get_user_portfolio(
          self,
          telegram_id: int,
          offset: int,
          limit: int
     ) -> DetailSchema | SkinsOnPageSchema[UserPortfolioSkinSchema]:
          response = await self.request(
               method="GET",
               url=self.url_builder("/user/portfolio"),
               query_arguments={
                    "telegram_id": telegram_id,
                    "offset": offset,
                    "limit": limit
               }
          )
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Get user portfolio error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          elif response.status_code == 400:
               return DetailSchema(detail="Портфолио пустое.")
          
          return SkinsOnPageSchema(
               pages=response.obj.get("pages"),
               current_page=response.obj.get("current_page"),
               skins=response.obj.get("skins"),
               skin_model=UserPortfolioSkinSchema
          )
          
     async def create_skin_at_user_portfolio(
          self,
          telegram_id: int,
          skin_name: str
     ) -> DetailSchema:
          response = await self.request(
               method="POST",
               url=self.url_builder("/user/portfolio"),
               query_arguments={
                    "telegram_id": telegram_id,
                    "skin_name": skin_name
               }
          )
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Create skin at user portfolio error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          elif response.status_code == 400:
               return DetailSchema(detail="Этот скин уже есть в вашем портфолио.")
          
          elif response.status_code == 200:
               return DetailSchema(detail="Скин добавлен в портфолио.")
          
          
     async def delete_skin_at_user_portfolio(
          self,
          telegram_id: int,
          skin_name: str
     ) -> DetailSchema:
          response = await self.request(
               method="DELETE",
               url=self.url_builder("/user/portfolio"),
               query_arguments={
                    "telegram_id": telegram_id,
                    "skin_name": skin_name
               }
          )
          if response.status_code in [422, 500]:
               logger.fastfy_client.error(msg=f"Delete skin at user portfolio error {response.status_code} {response.obj.get("detail")}")
               return DetailSchema(detail="Произошла ошибка. Повторите запрос позже.")
          
          elif response.status_code == 400:
               return DetailSchema(detail="Этот скин отсутствует в портфолио.")
          
          elif response.status_code == 200:
               return DetailSchema(detail="Скин удалён.")
          
     
     async def get_all_users_notifies(self) -> None | list[UserNotifySchema]:
          response = await self.request(
               method="GET",
               url=self.url_builder("/user/notify")
          )
          if response.status_code == 404:
               return []
          
          elif response.status_code in [500, 400]:
               logger.fastfy_client.error(msg=f"Get all users notifies error {response.status_code} {response.obj.get("detail")}")
               return None
          
          return [UserNotifySchema.model_validate(notify_obj) for notify_obj in response.obj]
          