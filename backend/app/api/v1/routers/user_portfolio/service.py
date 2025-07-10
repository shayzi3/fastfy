import uuid

from pydantic import UUID4

from app.infrastracture.https.steam import HttpSteamClient
from app.db.session import AsyncSession
from app.responses.abstract import AbstractResponse
from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel, UserPortfolioRelModel
from app.responses import (
     PortfolioSkinCreateSuccess, 
     SkinPortfolioAlreadyExists,
     PortfolioEmpty,
     SkinNotExists,
     SkinDeleteSuccess,
     SkinChangeSuccess,
     SkinNotFoundError
)
from app.db.repository import (
     UserPortfolioRepository, 
     SkinRepository, 
     SkinPriceHistoryRepository,
     NotifyRepository
)
from .schema import CreateUpdateSkin 



class UserPortfolioService:
     def __init__(self):
          self.portfolio_repository = UserPortfolioRepository
          self.skin_repository = SkinRepository
          self.skin_history_repository = SkinPriceHistoryRepository
          self.notify_repository = NotifyRepository
          self.steam_client = HttpSteamClient()
          
          
     async def get_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str
     ) -> list[UserPortfolioRelModel] | AbstractResponse:
          skins = await self.portfolio_repository.read_all(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"portfolio:{user_uuid}",
               user_uuid=user_uuid
          )
          if skins is None:
               return PortfolioEmpty
          return skins
     
     
     async def delete_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          skin_name: str | None,
          item_id: UUID4 | None
     ) -> AbstractResponse:
          delete_args = {
               "skin_name": skin_name,
               "user_uuid": user_uuid
          } if skin_name is not None else {
               "item_id": item_id
          }
          
          result = await self.portfolio_repository.delete(
               session=async_session,
               redis_session=redis_session,
               delete_redis_values=[
                    f"portfolio:{user_uuid}", 
                    f"portfolio_skin:{skin_name}@{user_uuid}"
               ],
               **delete_args
          )
          if result is False:
               return SkinNotExists
          return SkinDeleteSuccess
     
     
     async def patch_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          skin_data: CreateUpdateSkin,
          skin_name: str | None,
          item_id: UUID4 | None
     ) -> AbstractResponse:
          update_where = {
               "skin_name": skin_name,
               "user_uuid": user_uuid
          } if skin_name is not None else {
               "item_id": item_id
          }
          
          skin_update = await self.portfolio_repository.update(
               session=async_session,
               where=update_where,
               redis_session=redis_session,
               delete_redis_values=[
                    f"portfolio:{user_uuid}", 
                    f"portfolio_skin:{skin_name}@{user_uuid}"
               ],
               **skin_data.non_nullable()
          )
          if skin_update is False:
               return SkinNotFoundError
          return SkinChangeSuccess
          
          
     async def post_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          skin_data: CreateUpdateSkin,
          skin_name: str
     ) -> AbstractResponse | SkinModel:
          skin_exists =  await self.skin_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"skin:{skin_name}",
               name=skin_name
          )
          if skin_exists is not None:
               skin_exists_in_portfolio = await self.portfolio_repository.read(
                    session=async_session,
                    redis_session=redis_session,
                    redis_key=f"portfolio_skin:{skin_name}@{user_uuid}",
                    skin_name=skin_name,
                    user_uuid=user_uuid
               )
               if skin_exists_in_portfolio is None:
                    await self.portfolio_repository.create(
                         session=async_session,
                         redis_session=redis_session,
                         delete_redis_values=[f"portfolio:{user_uuid}"],
                         data={
                              "item_id": uuid.uuid4(),
                              "user_uuid": user_uuid,
                              "skin_name": skin_name,
                              **skin_data.non_nullable()
                         }
                    )
                    return PortfolioSkinCreateSuccess
               return SkinPortfolioAlreadyExists
          else:
               return await self.steam_client.skin_exists(skin_name=skin_name)
               
               
     async def _post_portfolio_create_skin(
          self, 
          async_session: AsyncSession,
          redis_session: RedisPool,
          skin: SkinModel,
          skin_data: CreateUpdateSkin,
          user_uuid: str
     ) -> None:
          try:
               await self.skin_repository.create(
                    session=async_session,
                    data=skin.model_dump()
               )
               skin_history = await self.steam_client.skin_price_history(
                    skin_name=skin.name
               )
               await self.skin_history_repository.create(
                    session=async_session,
                    data=skin_history
               )
               await self.portfolio_repository.create(
                    session=async_session,
                    redis_session=redis_session,
                    delete_redis_values=[f"portfolio:{user_uuid}"],
                    data={
                         "item_id": uuid.uuid4(),
                         "user_uuid": user_uuid,
                         "skin_name": skin.name,
                         **skin_data.non_nullable()
                    }
               )
               await self.notify_repository.create(
                    session=async_session,
                    redis_session=redis_session,
                    delete_redis_values=[f"notify_history:{user_uuid}"],
                    data={
                         "notify_id": uuid.uuid4(),
                         "user_uuid": user_uuid,
                         "text": f"Предмет {skin.name} добавлен успешно."
                    }
               )
          except:
               await self.notify_repository.create(
                    session=async_session,
                    redis_session=redis_session,
                    delete_redis_values=[f"notify_history:{user_uuid}"],
                    data={
                         "notify_id": uuid.uuid4(),
                         "user_uuid": user_uuid,
                         "text": f"Ошибка при добавлении предмета {skin.name}. Попробуйте ещё раз позже."
                    }
               )
          
     
     
async def get_user_portfolio_service():
     return UserPortfolioService()