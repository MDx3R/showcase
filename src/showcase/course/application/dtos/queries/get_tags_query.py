"""DTO for GetTags query."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GetTagsQuery:
    skip: int = 0
    limit: int = 100
