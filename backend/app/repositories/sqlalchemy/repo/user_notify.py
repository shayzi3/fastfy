from sqlalchemy import update

from app.db.models import UserNotify
from app.schemas.dto import UserNotifyDTO
from ..repository import SQLAlchemyRepository

from app.repositories.sqlalchemy.condition import SQLAlchemyWhereCondition
from app.schemas.enums import WhereConditionEnum



class SQLAlchemyUserNotifyRepository(SQLAlchemyRepository[UserNotifyDTO, UserNotify]):
     model = UserNotify