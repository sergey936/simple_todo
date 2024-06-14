from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class UserWithThatEmailAlreadyExists(LogicException):
    text: str

    @property
    def message(self):
        return f"User with email: {self.text} already exists"
