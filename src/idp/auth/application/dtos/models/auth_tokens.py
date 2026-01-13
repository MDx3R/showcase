from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class AuthTokens:
    access_token: str
    refresh_token: str

    @classmethod
    def create(cls, access_token: str, refresh_token: str) -> Self:
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
        )
