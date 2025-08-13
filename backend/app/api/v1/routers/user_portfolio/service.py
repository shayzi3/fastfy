import uuid

from app.infrastracture.https.steam import HttpSteamClient
from app.db.session import AsyncSession
from app.responses.abstract import AbstractResponse
from app.infrastracture.redis import RedisPool
from app.schemas import  UserSkinRelModel, SkinsPage
from app.responses import (
     PortfolioSkinCreateSuccess, 
     SkinPortfolioAlreadyExists,
     PortfolioEmpty,
     SkinNotExists,
     SkinDeleteSuccess,
     OffsetError
)
from app.db.repository import (
     UserSkinRepository, 
     SkinRepository, 
     SkinPriceHistoryRepository,
     UserNotifyRepository,
     SkinPriceInfoRepository
)


class UserPortfolioService:
     def __init__(self):
          self.portfolio_repository = UserSkinRepository
          self.skin_repository = SkinRepository
          self.skin_history_repository = SkinPriceHistoryRepository
          self.skin_price_repository = SkinPriceInfoRepository
          self.notify_repository = UserNotifyRepository
          self.steam_client = HttpSteamClient()
          
          
     async def get_portfolio(
          self,
          async_session: AsyncSession,
          redis_session: RedisPool,
          user_uuid: str,
          offset: int,
          limit: int
     ) -> SkinsPage | AbstractResponse:
          if offset % limit != 0:
               return OffsetError
               
          skins = await self.portfolio_repository.read_paginate(
               session=async_session,
               redis_session=redis_session,
               user_uuid=user_uuid,
               offset=offset,
               limit=limit
          )
          if not skins.skins:
               return PortfolioEmpty
          return skins
          
     
     
     async def delete_portfolio(
          self,
          async_session: AsyncSession,
          user_uuid: str,
          skin_name: str,
     ) -> AbstractResponse:
          result = await self.portfolio_repository.delete(
               session=async_session,
               user_uuid=user_uuid,
               skin_name=skin_name
          )
          if result is False:
               return SkinNotExists
          return SkinDeleteSuccess
          
          
     async def post_portfolio(
          self,
          async_session: AsyncSession,
          skin_name: str,
          user_uuid: str
     ) -> AbstractResponse:
          skin_exists_in_portfolio = await self.portfolio_repository.read(
               session=async_session,
               skin_name=skin_name,
               user_uuid=user_uuid
          )
          if skin_exists_in_portfolio is None:
               await self.portfolio_repository.create(
                    session=async_session,
                    uuid=uuid.uuid4(),
                    user_uuid=user_uuid,
                    skin_name=skin_name
               )
               return PortfolioSkinCreateSuccess
          return SkinPortfolioAlreadyExists
     
     
     async def _after_post_portfolio(
          self,
          async_session: AsyncSession,
          skin_name: str
     ) -> None:
          skin_exists = await self.skin_price_repository.read(
               session=async_session,
               skin_name=skin_name
          )
          if skin_exists is None:
               await self.skin_price_repository.create(
                    session=async_session,
                    skin_name=skin_name
               )
     
     
          
     
     
async def get_user_portfolio_service():
     return UserPortfolioService()