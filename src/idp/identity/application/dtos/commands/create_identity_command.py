from dataclasses import dataclass


@dataclass(frozen=True)
class CreateIdentityCommand:
    email: str
    username: str
    password: str
