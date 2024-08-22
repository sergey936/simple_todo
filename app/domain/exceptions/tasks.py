from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmptyTitleException(ApplicationException):

    @property
    def message(self):
        return "Task title cannot be empty"


@dataclass(eq=False)
class TitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return "Task title too long"


@dataclass(eq=False)
class TaskBodyTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return "Task body text too long"


@dataclass(eq=False)
class EmptyTaskBodyException(ApplicationException):

    @property
    def message(self):
        return "Task body text cannot be empty"


@dataclass(eq=False)
class InvalidImportanceException(ApplicationException):
    text: str

    @property
    def message(self):
        return "Importance should be from 1 to 10"


@dataclass(eq=False)
class EmptyImportanceException(ApplicationException):

    @property
    def message(self):
        return "Importance cannot be empty"


@dataclass(eq=False)
class InvalidDateException(ApplicationException):

    @property
    def message(self):
        return "Incorrect data. You can't complete a task in the past."


@dataclass(eq=False)
class EmptyTimeToCompleteException(ApplicationException):

    @property
    def message(self):
        return "Need to choose date."
