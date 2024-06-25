from datetime import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    oid: str
    username: str
    email: str
    password: str
    created_at: datetime
