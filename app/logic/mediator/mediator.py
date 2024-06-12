from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from logic.commands.base import CT, CR, BaseCommandHandler
from logic.events.base import ET, ER, BaseEventHandler, BaseEvent
from logic.exceptions.mediator import CommandHandlerNotRegistered
from logic.queries.base import QT, QR, BaseQueryHandler


@dataclass
class Mediator:
    commands_list: dict[CT, CR] = field(
        default_factory=lambda: defaultdict[list],
        kw_only=True
    )
    events_list: dict[ET, ER] = field(
        default_factory=lambda: defaultdict[list],
        kw_only=True
    )
    queries_list: dict[QT, QR] = field(
        default_factory=defaultdict,
        kw_only=True
    )

    # Register commands / queries / events
    def register_command(self, command: CT, command_handlers: Iterable[BaseCommandHandler[CT, CR]]):
        self.commands_list[command.__class__].extend(command_handlers)

    def register_event(self, event: ET, event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        self.events_list[event.__class__].extend(event_handlers)

    def register_query(self, query: QT, query_handlers: Iterable[BaseQueryHandler[QT, QR]]):
        self.queries_list[query.__class__].extend(query_handlers)

    # Handlers for commands / queries
    async def handle_command(self, command: CT) -> Iterable[CR]:
        handlers = self.commands_list[command.__class__]

        if not handlers:
            raise CommandHandlerNotRegistered(command.__class__)

        return [await handler.handle(command) for handler in handlers]

    async def handler_query(self, query: QT) -> QR:
        return self.queries_list[query.__class__].handle(query)

    # publish (handle event)
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[BaseEventHandler] = self.queries_list[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result


