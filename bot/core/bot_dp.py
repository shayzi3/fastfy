from aiogram import Dispatcher, Bot

from .config import my_config


bot = Bot(my_config.bot_token)
dp = Dispatcher()