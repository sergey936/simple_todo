from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.values.users import Password


@dataclass
class BasePasswordManager(ABC):
    @abstractmethod
    def hash_password(self, raw_password: str) -> str:
        ...

    @abstractmethod
    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        ...
