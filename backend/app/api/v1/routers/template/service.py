from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastracture.redis import RedisPool
from app.db.repository import UserRepository
from app.schemas import UserModel
from app.responses.abstract import AbstractResponse
from app.responses import isresponse, TokenError
from app.core.security import jwt_decode



class TemplateService:
     def __init__(self):
          self.user_repository = UserRepository
          
          
     async def profile(
          self, 
          redis_session: RedisPool,
          async_session: AsyncSession,
          uuid: str
     ) -> UserModel | AbstractResponse:
          user = await self.user_repository.read(
               session=async_session,
               redis_session=redis_session,
               redis_key=f"user:{uuid}",
               uuid=uuid
          )
          if user is None:
               return TokenError
          return user
     
     
async def get_template_service() -> TemplateService:
     return TemplateService()