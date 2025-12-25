# core/logger.py

from __future__ import annotations

import logging
import sys
from typing import Optional

from core.config import Config


_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Central logger factory.

    - Prevents duplicate handlers
    - Applies consistent formatting
    - Respects Config.LOG_LEVEL
    - CI-safe (stdout)
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    log_level = level or Config.LOG_LEVEL
    logger.setLevel(log_level)

    # --- Console handler (stdout, CI-friendly) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt=_LOG_FORMAT,
        datefmt=_DATE_FORMAT,
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- Optional file logging (disabled by default) ---
    if Config.LOG_FILE:
        file_handler = logging.FileHandler(Config.LOG_FILE, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False  # avoid duplicate root logs

    logger.debug(
        "Logger initialized | level=%s | file=%s",
        log_level,
        Config.LOG_FILE if Config.LOG_FILE else "stdout-only",
    )

    return logger
