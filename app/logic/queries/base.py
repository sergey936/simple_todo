from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Any, Generic

from logic.mediator.mediator import Mediator


@dataclass
class BaseQuery(ABC):
    ...


QT = TypeVar('QT', bound=BaseQuery)
QR = TypeVar('QR', bound=Any)


@dataclass
class BaseQueryHandler(ABC, Generic[QT, QR]):
    _mediator: Mediator

    async def handle(self, query: QT) -> QR:
        ...
