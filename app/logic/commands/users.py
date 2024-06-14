from dataclasses import dataclass

from domain.entities.users import User
from domain.values.users import Username, Password, Email
from infra.repositories.users.base import BaseUserRepository
from logic.commands.base import BaseCommand, BaseCommandHandler, CT, CR
from logic.exceptions.users import UserWithThatEmailAlreadyExists


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    username: str
    password: str
    email: str


@dataclass(frozen=True)
class CreateUserCommandHandler(BaseCommandHandler):
    user_repository: BaseUserRepository

    async def handle(self, command: CreateUserCommand) -> User:
        if await self.user_repository.check_user_by_email(email=command.email):
            raise UserWithThatEmailAlreadyExists(text=command.email)

        password = Password(value=command.password)
        username = Username(value=command.username)
        email = Email(value=command.email)

        new_user = User(
            password=password,
            username=username,
            email=email
        )

        await self.user_repository.register_user(new_user=new_user)

        return new_user

