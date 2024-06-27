from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseNotificator(ABC):

    @abstractmethod
    async def send_notification(self, recipient: str, subject: str, body: str) -> None:
        ...
