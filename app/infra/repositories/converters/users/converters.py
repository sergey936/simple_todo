from domain.entities.users import User
from domain.values.users import Email, Username, Password
from infra.db.models.user import Users
from infra.repositories.dtos.user import UserDTO


def convert_user_entity_to_dbmodel(user: User) -> Users:
    return Users(
        id=user.oid,
        name=user.username.as_generic_type(),
        email=user.email.as_generic_type(),
        password=user.password.as_generic_type(),
        created_at=user.created_at
    )


def convert_user_db_model_to_entity(user: Users) -> User:
    return User(
        oid=user.id,
        username=Username(user.name),
        email=Email(user.email),
        password=Password(user.password),
        created_at=user.created_at
    )
