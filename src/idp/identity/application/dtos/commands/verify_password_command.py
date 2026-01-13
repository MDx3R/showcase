from dataclasses import dataclass


@dataclass(frozen=True)
class VerifyPasswordCommand:
    email: str
    password: str
