from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class TaskNotFoundException(LogicException):
    task_oid: str

    @property
    def message(self):
        return f"Task with oid: {self.task_oid} not found."
