from pydantic_settings import SettingsConfigDict, BaseSettings


class Config(BaseSettings):
     postgres_url: str
     domain: str
     steam_api_key: str
     jwt_secret: str
     jwt_alghoritm: str
     bot_deep_link: str
     
     model_config = SettingsConfigDict(env_file="app/core/.env")
     
     @property
     def steam_return_to(self) -> str:
          return self.domain + "/api/v1/auth/SteamProcessing"
     
     @property
     def profile_url(self) -> str:
          return self.domain + "/main/profile"
     
     
my_config = Config()