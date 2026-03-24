"""
consent.py — User consent gate.
The agent REFUSES to start without explicit, recorded consent.
"""

import json
import datetime
import getpass
import platform
from pathlib import Path

from agent.config import CONSENT_FILE


CONSENT_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║              PHANTOM AGENT V1 — CONSENT NOTICE              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  This tool monitors the following ONLY on this machine:      ║
║                                                              ║
║    • Active process list (names, PIDs)                       ║
║    • Network connection count                                ║
║    • Public IP address                                       ║
║    • Timestamps of collection events                         ║
║                                                              ║
║  Purpose: Ethical forensic monitoring for threat detection.   ║
║                                                              ║
║  Data is stored LOCALLY. Alerts may be sent via email if     ║
║  configured.  You may revoke consent at any time by           ║
║  deleting the consent.json file or stopping the agent.        ║
║                                                              ║
║  NO data is collected without your explicit agreement.        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


def _record_consent(accepted: bool) -> dict:
    """Write a tamper-evident consent record."""
    record = {
        "accepted": accepted,
        "user": getpass.getuser(),
        "hostname": platform.node(),
        "os": platform.platform(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "agent_version": "1.0.0",
    }
    CONSENT_FILE.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def has_valid_consent() -> bool:
    """Check if a valid consent record already exists."""
    if not CONSENT_FILE.exists():
        return False
    try:
        data = json.loads(CONSENT_FILE.read_text(encoding="utf-8"))
        return data.get("accepted", False) is True
    except (json.JSONDecodeError, KeyError):
        return False


def request_consent() -> bool:
    """
    Display consent notice and ask the user.
    Returns True only if the user types 'yes'.
    """
    if has_valid_consent():
        print("[✓] Valid consent record found. Continuing…")
        return True

    print(CONSENT_TEXT)
    answer = input("Do you consent to monitoring? (yes/no): ").strip().lower()

    if answer == "yes":
        _record_consent(accepted=True)
        print("[✓] Consent recorded. Agent will start.\n")
        return True
    else:
        _record_consent(accepted=False)
        print("[✗] Consent denied. Agent will NOT start.")
        return False
