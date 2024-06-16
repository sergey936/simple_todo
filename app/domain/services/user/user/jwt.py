import jwt
from dataclasses import dataclass

from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from punq import Container

from logic.init import get_container
from settings.config import Config


# TODO make this on commands
@dataclass
class UserService:
    container: Container
    config: Config = container.resolve(Config)

    async def get_current_user(self, token: str = Depends(config.oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            username: str = payload.get("sub")

            if username is None:
                raise credentials_exception

        except InvalidTokenError:
            raise credentials_exception

        # TODO use repository
        user = get_user(fake_users_db, username=username)
        if user is None:
            raise credentials_exception
        return user

