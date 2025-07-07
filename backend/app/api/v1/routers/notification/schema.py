from pydantic import BaseModel, UUID4


class NotifyID(BaseModel):
     ids: list[UUID4]