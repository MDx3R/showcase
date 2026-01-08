"""JSON formatter for structured logging."""

import json
import logging
from datetime import UTC, datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Format log records as JSON."""

    def __init__(self, pretty: bool = False) -> None:
        """Initialize formatter.

        Args:
            pretty: Whether to pretty-print JSON output.

        """
        super().__init__()
        self.pretty = pretty

    def formatTime(self, record: logging.LogRecord, datefmt: Any = None) -> str:
        """Format timestamp in ISO format."""
        dt = datetime.fromtimestamp(record.created, UTC)
        return dt.isoformat()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_record: dict[str, Any] = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }

        if extra := getattr(record, "extra", None):
            log_record.update(extra)

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(
            log_record, indent=2 if self.pretty else None, ensure_ascii=False
        )
