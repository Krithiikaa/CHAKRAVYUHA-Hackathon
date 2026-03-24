"""
logger.py — CSV logging with time-based rotation.
Temp logs rotate (overwrite) every LOG_ROTATION_MINUTES.
"""

import csv
import time
import shutil
import datetime
from pathlib import Path

from agent.config import LOGS_DIR, LOG_ROTATION_MINUTES
from agent.collector import Snapshot

TEMP_LOG = LOGS_DIR / "temp_activity.csv"
CSV_FIELDS = ["timestamp", "process_count", "top_processes",
              "connection_count", "public_ip"]

_rotation_start: datetime.datetime | None = None

MAX_RETRIES = 3
RETRY_DELAY = 0.5  # seconds


def _ensure_header():
    """Write CSV header if file doesn't exist or is empty."""
    if not TEMP_LOG.exists() or TEMP_LOG.stat().st_size == 0:
        with open(TEMP_LOG, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=CSV_FIELDS).writeheader()


def write_snapshot(snap: Snapshot) -> Path:
    """Append a snapshot row to the temp CSV (with retry for file locks)."""
    _ensure_header()
    for attempt in range(MAX_RETRIES):
        try:
            with open(TEMP_LOG, "a", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=CSV_FIELDS).writerow(snap.to_flat_row())
            return TEMP_LOG
        except PermissionError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"[⚠] CSV write failed after {MAX_RETRIES} retries (file locked)")
    return TEMP_LOG


def should_rotate() -> bool:
    """Check if LOG_ROTATION_MINUTES have passed since last rotation."""
    global _rotation_start
    now = datetime.datetime.now(datetime.timezone.utc)
    if _rotation_start is None:
        _rotation_start = now
        return False
    elapsed = (now - _rotation_start).total_seconds() / 60
    return elapsed >= LOG_ROTATION_MINUTES


def rotate_log() -> Path | None:
    """
    Archive the current temp log and start fresh.
    Returns the archived path (for evidence capture) or None.
    """
    global _rotation_start
    if not TEMP_LOG.exists():
        return None

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive = LOGS_DIR / f"activity_{ts}.csv"
    shutil.copy2(TEMP_LOG, archive)

    # Overwrite temp with fresh header
    with open(TEMP_LOG, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CSV_FIELDS).writeheader()

    _rotation_start = datetime.datetime.now(datetime.timezone.utc)
    return archive


def get_current_log() -> Path:
    """Return path to the current temp log."""
    _ensure_header()
    return TEMP_LOG
