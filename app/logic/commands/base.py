from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Any, Generic

from logic.mediator.mediator import Mediator


@dataclass(frozen=True)
class BaseCommand(ABC):
    ...


CT = TypeVar('CT', bound=BaseCommand)
CR = TypeVar('CR', bound=Any)


@dataclass
class BaseCommandHandler(ABC, Generic[CT, CR]):
    _mediator: Mediator

    async def handle(self, command: CT) -> CR:
        ...
