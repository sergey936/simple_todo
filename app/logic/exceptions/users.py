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
class UserNotFound(LogicException):
    text: str

    @property
    def message(self):
        return f"User with email: {self.text} not found"
