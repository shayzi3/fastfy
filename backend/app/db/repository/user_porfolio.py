import json
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.schemas import UserPortfolioModel, UserPortfolioRelModel
from app.db.models import UsersPortfolio
from app.db.session import AsyncSession, Session
from app.infrastracture.redis import RedisPool

from .base import BaseRepository



class UserPortfolioRepository(
     BaseRepository[UserPortfolioModel, UserPortfolioRelModel]
):
     model = UsersPortfolio
     
     
     @classmethod
     async def read_all(
          cls,
          session: AsyncSession,
          redis_session: RedisPool,
          redis_key: str,
          **read_args
     ) -> list[UserPortfolioRelModel] | None:
          result = await redis_session.get(redis_key)
          if result is not None:
               result = json.loads(result)
               return [
                    UserPortfolioRelModel.model_validate(model)
                    for model in result
               ]
          
          sttm = (
               select(UsersPortfolio).
               filter_by(**read_args).
               options(selectinload(UsersPortfolio.skin))
          )
          result = await session.execute(sttm)
          result = result.scalars().all()

          if not result:
               return None
          
          result = [
               UserPortfolioRelModel.model_validate(model, from_attributes=True)
               for model in result
          ]
          await redis_session.set(
               name=redis_key,
               value=json.dumps([model.model_dump() for model in result]),
               ex=1000
          )
          return result
          
          
     @classmethod
     async def read_all_task(cls) -> list[UsersPortfolio]:
          async with Session.session() as async_session:
               sttm = (
                    select(UsersPortfolio).
                    options(selectinload(UsersPortfolio.skin), selectinload(UsersPortfolio.user))
               )
               result = await async_session.execute(sttm)
               result = result.scalars().all()
          return result
          
          