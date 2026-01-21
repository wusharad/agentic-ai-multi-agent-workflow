import logging
import sys
from logging.handlers import RotatingFileHandler

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "trace_id=%(trace_id)s | %(message)s"
)

def setup_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(LOG_FORMAT)

    # =========================
    # Console Handler (UTF-8)
    # =========================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # =========================
    # File Handler (UTF-8 safe)
    # =========================
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8"   # 🔥 CRITICAL FIX
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return root_logger