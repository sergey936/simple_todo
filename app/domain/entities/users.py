from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.users import NewUserCreatedEvent
from domain.values.users import Username, Email, Password


@dataclass
class User(BaseEntity):
    username: Username
    email: Email
    password: Password

    @classmethod
    def create_user(
            cls,
            username: Username,
            email: Email,
            password: Password
    ) -> 'User':
        new_user = User(
            username=username,
            email=email,
            password=password
        )
        new_user.register_event(
            NewUserCreatedEvent(
                username=new_user.username.as_generic_type(),
                user_oid=new_user.oid,
                user_email=new_user.email.as_generic_type()
            )
        )
        return new_user
