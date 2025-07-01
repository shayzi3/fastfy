from typing import Union

from app.schemas import TokenPayload
from app.responses.abstract import AbstractResponse



TokenData = Union[TokenPayload, AbstractResponse]