from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Any, Generic

from logic.mediator.mediator import Mediator


@dataclass
class BaseEvent(ABC):
    ...


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[ET, ER]):
    _mediator: Mediator

    async def handle(self, event: ET) -> ER:
        ...
