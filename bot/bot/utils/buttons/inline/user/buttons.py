from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas.fastfy import SkinsOnPageSchema, SkinSchema, UserPortfolioSkinSchema
from bot.utils.compress import CompressName
from bot.utils.filters.user.callback_data import Skin, Paginate



def login_button(url: str) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     builder.add(
          InlineKeyboardButton(
               text="Войти через Steam",
               url=url
          )
     )
     return builder.as_markup()


def profile_button() -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     builder.add(
          InlineKeyboardButton(
               text="Изменить процент",
               callback_data="change_user_percent"
          )
     )
     return builder.as_markup()


def paginate_buttons(
     skins: SkinsOnPageSchema,
     paginate_component: str,
     offset: int = 0,
     query: str = ""
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     for skin in skins.skins:
          skin_name = getattr(skin, "skin_name", None) or getattr(skin, "name", None)
          compress_name = CompressName.compress(skin_name, "to")
          builder.add(
               InlineKeyboardButton(
                    text=compress_name,
                    callback_data=Skin(
                         skin_name=compress_name,
                         mode=paginate_component
                    ).pack()
               )
          )
          
     builder.add(
          InlineKeyboardButton(
               text="<",
               callback_data=Paginate(
                    offset=offset,
                    mode=paginate_component,
                    query=query,
                    vector="left"
               ).pack()
          ),
          InlineKeyboardButton(
               text=f"{skins.current_page}/{skins.pages}",
               callback_data="empty"
          ),
          InlineKeyboardButton(
               text=">",
               callback_data=Paginate(
                    offset=offset,
                    mode=paginate_component,
                    query=query,
                    vector="right"
               ).pack()
          )
     )
     builder.adjust(*[1 for _ in skins.skins], 3)
     return builder.as_markup()