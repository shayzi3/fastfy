from bot.schemas.fastfy import (
     UserSchema,
     DetailSchema,
     SkinsOnPageSchema,
     SkinSteamInventorySchema,
     UserPortfolioSkinSchema,
     UserNotifySchema
)
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
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
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
          return DetailSchema.model_validate(response.obj)
     
     
     async def get_user_steam_inventory(
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
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
          
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
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
          
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
          return DetailSchema.model_validate(response.obj)
          
          
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
          return DetailSchema.model_validate(response.obj)
     
     
     async def get_all_users_notifies(self) -> DetailSchema | list[UserNotifySchema]:
          response = await self.request(
               method="GET",
               url=self.url_builder("/user/notify")
          )
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
          return [UserNotifySchema.model_validate(notify_obj) for notify_obj in response.obj]
          