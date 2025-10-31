import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL


load_dotenv()


class Config:
     ps_username: str = str(os.environ.get("PS_USERNAME"))
     ps_password: str = str(os.environ.get("PS_PASSWORD"))
     ps_domain: str = str(os.environ.get("PS_DOMAIN"))
     ps_port: str = str(os.environ.get("PS_PORT"))
     ps_database_name: str = str(os.environ.get("PS_DATABASE_NAME"))
     domain: str = str(os.environ.get("DOMAIN"))
     steam_api_key: str = str(os.environ.get("STEAM_API_KEY"))
     secret_bot_token: str = str(os.environ.get("SECRET_BOT_TOKEN"))
     redis_host: str = str(os.environ.get("REDIS_HOST"))
     redis_port: int = int(os.environ.get("REDIS_PORT"))
     redis_password: str = str(os.environ.get("REDIS_PASSWORD"))
     data_path: str = str(os.environ.get("DATA_PATH"))
     local_host: str = str(os.environ.get("LOCAL_HOST"))
     jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")
     jwt_algorithm: str = os.environ.get("JWT_ALGORITHM")
     
     
     @property
     def steam_return_to(self) -> str:
          return self.domain + "/api/v1/auth/steam/processing"
     
     @property
     def postgres_url(self) -> str:
          return URL.create(
               drivername="postgresql+asyncpg",
               username=self.ps_username,
               password=self.ps_password,
               host=self.ps_domain,
               port=self.ps_port,
               database=self.ps_database_name
          ).render_as_string(hide_password=False)
     
my_config = Config()