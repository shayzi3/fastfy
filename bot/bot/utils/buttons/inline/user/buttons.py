from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



def login_button(url: str) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     builder.add(
          InlineKeyboardButton(
               text="Войти через Steam",
               url=url
          )
     )
     return builder.as_markup()