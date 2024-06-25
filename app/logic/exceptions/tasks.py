from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class TaskNotFoundException(LogicException):
    task_oid: str

    @property
    def message(self):
        return f"Task with oid: {self.task_oid} not found."


@dataclass
class TaskAccessDeniedException(LogicException):

    @property
    def message(self):
        return "Access denied. It's not your task."


@dataclass
class GetAllTasksAccessDenied(LogicException):

    @property
    def message(self):
        return "Access denied. You cant read other users tasks."


