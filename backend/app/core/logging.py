"""Structured (JSON) logging."""

import json
import logging
import sys
from datetime import UTC, datetime

# Attributes present on every LogRecord; anything else came in through ``extra=``.
_STANDARD_ATTRS = set(vars(logging.LogRecord("", 0, "", 0, "", (), None))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(
            {k: v for k, v in record.__dict__.items() if k not in _STANDARD_ATTRS}
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    # Uvicorn's access log would duplicate (and not match) our request log.
    logging.getLogger("uvicorn.access").disabled = True
    # SQLAlchemy echo would print statements with data; keep it quiet.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
