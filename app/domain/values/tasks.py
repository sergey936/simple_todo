from dataclasses import dataclass

from domain.exceptions.tasks import EmptyTitleException, TitleTooLongException, EmptyTaskBodyException, \
    TaskBodyTooLongException, InvalidImportanceException, EmptyImportanceException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Title(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTitleException

        if len(self.value) > 80:
            raise TitleTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class TaskBody(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTaskBodyException

        if len(self.value) > 4000:
            raise TaskBodyTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Importance(BaseValueObject):
    def validate(self) -> None:
        if not self.value:
            raise EmptyImportanceException

        if not 0 < int(self.value) <= 10:
            raise InvalidImportanceException(self.value)

    def as_generic_type(self):
        return int(self.value)
