from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    secret_key: str = Field(default='', alias='SECRET_KEY')
    algorithm: str = Field(default='', alias='ALGORITHM')
    token_expire_min: int = Field(default=30, alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    database_url: str = Field(default='postgresql+asyncpg://postgres:rootroot@db_app:5432/Todo', alias='DATABASE_URL')

    class Config:
        env_file = ".env"


