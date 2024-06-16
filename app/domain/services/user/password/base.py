from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.values.users import Password


@dataclass
class BasePasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, raw_password: str) -> Password:
        ...

    @abstractmethod
    def verify_password(self, raw_password: str, hashed_password: Password) -> bool:
        ...
