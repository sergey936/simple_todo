from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class LogicException(ApplicationException):

    @property
    def message(self):
        return "Logic exceptions"
