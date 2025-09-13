import os

from dotenv import load_dotenv


load_dotenv(dotenv_path=None)



class Config:
     bot_token: str = os.environ.get("BOT_TOKEN")
     fastfy_base_url: str = os.environ.get("FASTFY_BASE_URL")
     fastfy_secret_bot_token = os.environ.get("FASTFY_SECRET_BOT_TOKEN")
     alert_chat = os.environ.get("ALERT_CHAT")
     data_path = os.environ.get("DATA_PATH")