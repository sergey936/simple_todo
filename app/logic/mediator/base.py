from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from logic.commands.base import CT, CR, BaseCommandHandler, BaseCommand
from logic.events.base import ET, ER, BaseEventHandler, BaseEvent
from logic.exceptions.mediator import CommandHandlerNotRegistered
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import QT, QR, BaseQueryHandler, BaseQuery


@dataclass(eq=False)
class Mediator(EventMediator, CommandMediator, QueryMediator):
    events_maps: dict[ET, BaseEventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    commands_map: dict[CT, BaseCommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[BaseEventHandler[ET, ER]]):
        self.events_maps[event].extend(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[BaseCommandHandler[CT, CR]]):
        self.commands_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[BaseEventHandler] = self.events_maps[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlerNotRegistered(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)
