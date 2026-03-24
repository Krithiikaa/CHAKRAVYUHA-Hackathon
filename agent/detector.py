"""
detector.py — Rule-based anomaly detection engine.
Evaluates each snapshot against configurable threat rules.
"""

import datetime
from collections import Counter
from dataclasses import dataclass, field
from typing import List

from agent.collector import Snapshot
from agent.config import (
    SUSPICIOUS_PROCESSES,
    CONNECTION_THRESHOLD,
    SUSPICIOUS_PROCESS_THRESHOLD,
)


@dataclass
class ThreatAlert:
    """Represents a detected anomaly."""
    rule: str
    severity: str            # LOW, MEDIUM, HIGH, CRITICAL
    description: str
    details: dict
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
    )


# ── In-memory state for cross-cycle detection ────────────
_process_history: List[List[str]] = []
_simulated_login_failures: int = 0


def simulate_login_failure():
    """
    Call this to simulate a failed login attempt.
    Used for demo/hackathon to trigger the login-attempt rule.
    """
    global _simulated_login_failures
    _simulated_login_failures += 1


def reset_login_failures():
    global _simulated_login_failures
    _simulated_login_failures = 0


def analyse(snapshot: Snapshot) -> List[ThreatAlert]:
    """Run all detection rules against a snapshot. Returns alerts."""
    alerts: List[ThreatAlert] = []

    # ── Rule 1: Suspicious process detected repeatedly ───
    _process_history.append(snapshot.process_names)
    if len(_process_history) > 10:
        _process_history.pop(0)

    # Flatten recent history and count
    flat = [n for cycle in _process_history for n in cycle]
    counts = Counter(flat)
    for proc_name in SUSPICIOUS_PROCESSES:
        if counts.get(proc_name, 0) >= SUSPICIOUS_PROCESS_THRESHOLD:
            alerts.append(ThreatAlert(
                rule="SUSPICIOUS_PROCESS_REPEAT",
                severity="HIGH",
                description=f"Suspicious process '{proc_name}' detected "
                            f"{counts[proc_name]} times in recent cycles",
                details={"process": proc_name, "count": counts[proc_name]},
            ))

    # ── Rule 2: High connection count ────────────────────
    if snapshot.connections > CONNECTION_THRESHOLD:
        alerts.append(ThreatAlert(
            rule="HIGH_CONNECTION_COUNT",
            severity="MEDIUM",
            description=f"Active connections ({snapshot.connections}) "
                        f"exceed threshold ({CONNECTION_THRESHOLD})",
            details={
                "connections": snapshot.connections,
                "threshold": CONNECTION_THRESHOLD,
            },
        ))

    # ── Rule 3: Simulated multiple login failures ────────
    global _simulated_login_failures
    if _simulated_login_failures >= 3:
        alerts.append(ThreatAlert(
            rule="MULTIPLE_LOGIN_FAILURES",
            severity="CRITICAL",
            description=f"{_simulated_login_failures} failed login attempts "
                        f"detected (simulated)",
            details={"attempts": _simulated_login_failures},
        ))
        _simulated_login_failures = 0  # reset after alert

    return alerts
