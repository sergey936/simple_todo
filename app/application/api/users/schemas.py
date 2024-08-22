from pydantic import BaseModel

from domain.entities.users import User


class ErrorSchema(BaseModel):
    error: str


class UserDetailSchema(BaseModel):
    oid: str
    username: str
    email: str

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            oid=user.oid,
            username=user.username.as_generic_type(),
            email=user.email.as_generic_type()
        )


class UserDeleteSchema(BaseModel):
    response: str = 'User deleted'


class CreateUserSchema(BaseModel):
    password: str
    email: str
    username: str


class UserEditResponseSchema(BaseModel):
    response: str = 'User edited'


class EditUserSchema(BaseModel):
    name: str | None = None
    password: str | None = None
    email: str | None = None
