import asyncio
import uuid

from app.infrastracture.https.steam import HttpSteamClient

from app.db.session import AsyncSession, Session
from app.responses.abstract import AbstractResponse
from app.infrastracture.redis import RedisPool
from app.schemas import SkinModel, UserPortfolioRelModel
from app.responses import (
     PortfolioSkinCreateSuccess, 
     SkinPortfolioAlreadyExists,
     PortfolioEmpty
)
from app.db.repository import (
     UserPortfolioRepository, 
     SkinRepository, 
     SkinPriceHistoryRepository
)

from .schema import CreateUpdateSkin



class UserPortfolioService:
     def __init__(self):
          self.portfolio_repository = UserPortfolioRepository
          self.skin_repository = SkinRepository
          self.skin_history_repository = SkinPriceHistoryRepository
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
          
          
     async def post_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          skin_data: CreateUpdateSkin,
          skin_name: str
     ) -> AbstractResponse:
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
                    redis_key=f"portfolio_skin:{skin_name}",
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
                              "quantity": skin_data.quantity,
                              "buy_price": skin_data.buy_price
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
                    "quantity": skin_data.quantity,
                    "buy_price": skin_data.buy_price
               }
          )
          
     
     
async def get_user_portfolio_service():
     return UserPortfolioService()