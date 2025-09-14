from typing import Literal
from aiogram.filters.callback_data import CallbackData

from aiogram_tool.callback_data import LongCallbackData


class Skin(LongCallbackData, prefix="&"):
     mode: str
     skin_name: str
     
     
class Paginate(CallbackData, prefix="&"):
     mode: str
     vector: Literal["left", "right"]
     offset: int
     query: str = ""