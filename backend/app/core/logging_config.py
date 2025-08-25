import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_level: int = logging.INFO) -> None:
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(ch_formatter)

    # File handler (rotating)
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = RotatingFileHandler(log_dir / "app.log", maxBytes=1_000_000, backupCount=3)
    fh.setLevel(log_level)
    fh.setFormatter(ch_formatter)

    # Avoid duplicate handlers during reload
    logger.handlers = [ch, fh]
