"""
evidence.py — Evidence packaging on anomaly detection.
Captures screenshot, moves logs, generates metadata, and hashes everything.
"""

import json
import shutil
import datetime
from pathlib import Path
from typing import List

from PIL import ImageGrab

from agent.config import EVIDENCE_DIR
from agent.logger import get_current_log
from agent.integrity import write_checksums
from agent.detector import ThreatAlert


def _create_incident_dir() -> Path:
    """Create a timestamped incident directory."""
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    incident_dir = EVIDENCE_DIR / f"incident_{ts}"
    incident_dir.mkdir(parents=True, exist_ok=True)
    return incident_dir


def capture_screenshot(dest_dir: Path) -> Path:
    """Take a screenshot and save to the incident directory."""
    screenshot_path = dest_dir / "screenshot.png"
    try:
        img = ImageGrab.grab()
        img.save(screenshot_path)
    except Exception as e:
        # Fallback: write a placeholder if display not available
        screenshot_path.write_text(
            f"[Screenshot unavailable: {e}]", encoding="utf-8"
        )
    return screenshot_path


def move_logs(dest_dir: Path) -> Path:
    """Copy current activity log to the incident directory."""
    src = get_current_log()
    dest = dest_dir / "activity_log.csv"
    if src.exists():
        shutil.copy2(src, dest)
    return dest


def generate_metadata(
    dest_dir: Path,
    alerts: List[ThreatAlert],
    snapshot_data: dict,
) -> Path:
    """Create a metadata.json summarising the incident."""
    meta = {
        "incident_id": dest_dir.name,
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "alert_count": len(alerts),
        "alerts": [
            {
                "rule": a.rule,
                "severity": a.severity,
                "description": a.description,
                "details": a.details,
                "timestamp": a.timestamp,
            }
            for a in alerts
        ],
        "snapshot_summary": snapshot_data,
        "integrity": "sha256_checksums_attached",
    }
    meta_path = dest_dir / "metadata.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta_path


def package_evidence(
    alerts: List[ThreatAlert],
    snapshot_data: dict,
) -> Path:
    """
    Full evidence packaging pipeline:
    1. Create incident directory
    2. Capture screenshot
    3. Move activity logs
    4. Generate metadata JSON
    5. Hash all files (SHA-256)
    """
    incident_dir = _create_incident_dir()

    capture_screenshot(incident_dir)
    move_logs(incident_dir)
    generate_metadata(incident_dir, alerts, snapshot_data)
    write_checksums(incident_dir)

    print(f"[📁] Evidence packaged → {incident_dir}")
    return incident_dir
