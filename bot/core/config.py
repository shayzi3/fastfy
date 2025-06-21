from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):
     bot_token: str
     secret_token: str
     webhook_url: str
     
     model_config = SettingsConfigDict(env_file="core/.env")
     
     
my_config = Config()