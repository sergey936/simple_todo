import hashlib
from dataclasses import dataclass

from domain.services.user.password.base import BasePasswordManager


@dataclass
class PasswordManager(BasePasswordManager):

    def hash_password(self, raw_password: str) -> str:
        hashed = hashlib.sha256(raw_password.encode()).hexdigest()
        return hashed

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return self.hash_password(raw_password) == hashed_password
