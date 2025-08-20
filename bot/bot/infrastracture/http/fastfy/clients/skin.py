from bot.schemas.fastfy import (
     DetailSchema, 
     SkinSchema, 
     SkinsOnPageSchema,
     SkinPriceHistorySchema
)
from ..base import HttpClient



class SkinClient(HttpClient):
     
     async def get_skin(
          self,
          skin_name: str
     ) -> DetailSchema | SkinSchema:
          response = await self.request(
               method="GET",
               url=self.url_builder(path="/skin"),
               query_arguments={"skin_name": skin_name}
          )
          if response.status_code == 404:
               return DetailSchema(detail=f"Скин {skin_name} не найден.")
          
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
          return SkinSchema.model_validate(response.obj)
     
     
     async def search_skins(
          self,
          offset: int,
          limit: int,
          query: str
     ) -> DetailSchema | SkinsOnPageSchema[SkinSchema]:
          response = await self.request(
               method="GET",
               url=self.url_builder("/skin/search"),
               query_arguments={
                    "offset": offset,
                    "limit": limit,
                    "query": query
               }
          )
          if response.status_code == 404:
               return DetailSchema(detail=f"По запросу {query} ничего не найдено.")
          
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)

          return SkinsOnPageSchema(
               pages=response.obj.get("pages"),
               current_page=response.obj.get("current_page"),
               skins=response.obj.get("skins"),
               skin_model=SkinSchema
          )
          
     
     async def price_history_skin(
          self,
          skin_name: str
     ) -> DetailSchema | None:
          response = await self.request(
               method="GET",
               url=self.url_builder("/skin/history"),
               query_arguments={"skin_name": skin_name}
          )
          if response.status_code == 404:
               return DetailSchema(detail=f"Скин {skin_name} не найден.")
          
          if "detail" in response.obj.keys():
               return DetailSchema.model_validate(response.obj)
          return SkinPriceHistorySchema.model_validate(response.obj)
          
               
          
     
     