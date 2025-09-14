from typing import Any

from aiogram.filters.callback_data import CallbackData




class CallbackDataStorage(CallbackData):
     _storage: dict[str, Any] = {}