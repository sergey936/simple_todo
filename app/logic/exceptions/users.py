from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class UserWithThatEmailAlreadyExists(LogicException):
    text: str

    @property
    def message(self):
        return f"User with email: {self.text} already exists"


@dataclass
class WrongPasswordException(LogicException):

    @property
    def message(self):
        return "Wrong password"


@dataclass
class UserNotFoundByIdException(LogicException):
    user_oid: str

    @property
    def message(self):
        return f"User with oid: {self.user_oid} not found"


@dataclass
class UserNotFoundByEmailException(LogicException):
    email: str

    @property
    def message(self):
        return f"User with email: {self.email} not found"


@dataclass
class IncorrectEmailOrPasswordException(LogicException):

    @property
    def message(self):
        return "Incorrect email or password"

