"""DTO for CreateTag command."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CreateTagCommand:
    name: str
