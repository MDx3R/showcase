"""Telegram bot configuration."""

from pydantic import BaseModel


class TelegramConfig(BaseModel):
    """Telegram bot configuration."""

    token: str
    enabled: bool = True
