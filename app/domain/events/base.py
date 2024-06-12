from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar
from uuid import uuid4


@dataclass(frozen=True)
class BaseEvent(ABC):
    event_title: ClassVar[str]

    event_id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )
