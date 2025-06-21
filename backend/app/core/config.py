from pydantic_settings import SettingsConfigDict, BaseSettings


class Config(BaseSettings):
     postgres_url: str
     steam_redirect_auth: str
     steam_return_to: str
     steam_api_key: str
     jwt_secret: str
     jwt_alghoritm: str
     bot_deep_link: str
     
     model_config = SettingsConfigDict(env_file="app/core/.env")
     
     
my_config = Config()