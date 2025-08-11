from pydantic_settings import SettingsConfigDict, BaseSettings


class Config(BaseSettings):
     postgres_url: str
     domain: str
     steam_api_key: str
     secret_bot_token: str
     
     model_config = SettingsConfigDict(env_file="app/core/.env")
     
     @property
     def steam_return_to(self) -> str:
          return self.domain + "/api/v1/auth/steam/processing"
     
my_config = Config()