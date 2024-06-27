from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    secret_key: str = Field(default='', alias='SECRET_KEY')
    algorithm: str = Field(default='', alias='ALGORITHM')
    token_expire_min: int = Field(default=30, alias='ACCESS_TOKEN_EXPIRE_MINUTES')

    database_url: str = Field(default='', alias='DATABASE_URL')

    smpt_server: str = Field(default='', alias="SMPT_HOST")
    smpt_port: int = Field(default='', alias="SMPT_PORT")
    smpt_user: str = Field(default='', alias="SMPT_USER")
    smpt_password: str = Field(default='', alias="SMPT_PASS")

    class Config:
        env_file = ".env"


