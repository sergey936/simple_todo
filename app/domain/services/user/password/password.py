import hashlib
from dataclasses import dataclass

from domain.services.user.password.base import BasePasswordHasher
from domain.values.users import Password


@dataclass
class PasswordHasher(BasePasswordHasher):

    def hash_password(self, raw_password: str) -> Password:
        hashed = hashlib.sha256(raw_password.encode()).hexdigest()
        return Password(hashed)

    def verify_password(self, raw_password: str, hashed_password: Password) -> bool:
        return PasswordHasher.hash_password(raw_password) == hashed_password
