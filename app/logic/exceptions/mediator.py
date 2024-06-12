from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass
class CommandHandlerNotRegistered(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Cant find command handler for command {self.command_type}"
