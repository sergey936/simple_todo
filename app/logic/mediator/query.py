from abc import abstractmethod
from dataclasses import dataclass, field

from logic.queries.base import QT, QR, BaseQueryHandler, BaseQuery


@dataclass(eq=False)
class QueryMediator:
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR:
        ...
