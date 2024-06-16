from fastapi.security import OAuth2PasswordBearer
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/users/token")

    secret_key: str = Field(default='', alias='SECRET_KEY')
    algorithm: str = Field(default='', alias='ALGORITHM')
    token_expire_min: int = Field(default='', alias='ACCESS_TOKEN_EXPIRE_MINUTES')

