from aiogram import Dispatcher, Bot

from .config import Config


bot = Bot(Config.bot_token)
dp = Dispatcher()