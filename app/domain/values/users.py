import hashlib
from dataclasses import dataclass

from domain.exceptions.users import (
    EmptyUsernameException, InvalidEmailException,
    EmptyPasswordException, UsernameTooLongException,
    EmailTooSmallException, EmailTooLongException, EmptyEmailException
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Password(BaseValueObject):

    def validate(self) -> None:
        if not self.value:
            raise EmptyPasswordException()

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Username(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyUsernameException()

        if len(self.value) > 30:
            raise UsernameTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyEmailException()

        if '@' not in self.value:
            raise InvalidEmailException(self.value)

        if len(self.value) < 4:
            raise EmailTooSmallException(self.value)

        if len(self.value) > 256:
            raise EmailTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)
