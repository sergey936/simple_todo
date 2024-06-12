from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyPasswordException(ApplicationException):

    @property
    def message(self):
        return 'Password cannot be empty'


@dataclass(eq=False)
class PasswordTooSmallException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Password too small'


@dataclass(eq=False)
class PasswordTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Password too long'


@dataclass(eq=False)
class EmptyUsernameException(ApplicationException):

    @property
    def message(self):
        return 'Username cannot be empty'


@dataclass(eq=False)
class UsernameTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Username too long'


@dataclass(eq=False)
class EmptyEmailException(ApplicationException):

    @property
    def message(self):
        return 'Email cannot be empty'


@dataclass(eq=False)
class EmailTooSmallException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Email too small'


@dataclass(eq=False)
class EmailTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Email too long'


@dataclass(eq=False)
class InvalidEmailException(ApplicationException):
    text: str

    @property
    def message(self):
        return 'Invalid email'
