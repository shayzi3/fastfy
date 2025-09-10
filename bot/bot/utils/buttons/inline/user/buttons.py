from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas.fastfy import SkinsOnPageSchema, SkinSchema
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
          builder.add(
               InlineKeyboardButton(
                    text=CompressName.compress(skin_name, "to"),
                    callback_data=Skin(
                         skin_name=CompressName.compress(
                              skin_name=skin_name,
                              mode="to",
                              callback_data=True
                         ),
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


def skin_portfolio_buttons(skin: SkinSchema) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Удалить предмет",
               callback_data=Skin(
                    mode="delete_portfolio_skin",
                    skin_name=CompressName.compress(
                         skin_name=skin.name,
                         mode="to",
                         callback_data=True
                    )
               ).pack()
          ),
          InlineKeyboardButton(
               text="📉 История цены",
               callback_data=Skin(
                    mode="history_portfolio_skin",
                    skin_name=CompressName.compress(
                         skin_name=skin.name,
                         mode="to",
                         callback_data=True
                    )
               ).pack()
          ),
          InlineKeyboardButton(
               text="Убрать это сообщение",
               callback_data="delete_message"
          )
     )
     builder.adjust(1, 1, 1)
     return builder.as_markup()