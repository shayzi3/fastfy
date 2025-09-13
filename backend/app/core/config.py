import os

from load_dotenv import load_dotenv


load_dotenv()


class Config:
     postgres_url: str = str(os.environ.get("POSTGRES_URL"))
     domain: str = str(os.environ.get("DOMAIN"))
     steam_api_key: str = str(os.environ.get("STEAM_API_KEY"))
     secret_bot_token: str = str(os.environ.get("SECRET_BOT_TOKEN"))
     redis_host: str = str(os.environ.get("REDIS_HOST"))
     redis_port: int = int(os.environ.get("REDIS_PORT"))
     redis_password: str = str(os.environ.get("REDIS_PASSWORD"))
     data_path: str = str(os.environ.get("DATA_PATH"))
     
     
     @property
     def steam_return_to(self) -> str:
          return self.domain + "/api/v1/auth/steam/processing"
     
my_config = Config()