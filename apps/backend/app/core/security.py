from typing import Any


def get_password_hash(value: str) -> str:
    # TODO: Implement password hashing when authentication is introduced.
    raise NotImplementedError


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # TODO: Implement password verification when authentication is introduced.
    raise NotImplementedError


def create_access_token(payload: dict[str, Any]) -> str:
    # TODO: Implement token creation when authentication is introduced.
    raise NotImplementedError

