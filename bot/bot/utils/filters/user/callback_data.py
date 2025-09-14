from typing import Any, Literal
from aiogram.filters.callback_data import CallbackData

# from bot.utils.callback_data_storage import CallbackDataStorage



class Skin(CallbackData, prefix="?"):
     mode: str
     skin_name: str
     
     
class Paginate(CallbackData, prefix="&"):
     mode: str
     vector: Literal["left", "right"]
     offset: int
     query: str = ""
     
     
skin = Skin(mode="mode", skin_name="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")