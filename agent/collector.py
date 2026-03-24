"""
collector.py — System telemetry collection.
Gathers processes, network connections, public IP, and timestamps.
"""

import datetime
from dataclasses import dataclass, field
from typing import List, Tuple

import psutil
import httpx


@dataclass
class Snapshot:
    """Single point-in-time system snapshot."""
    timestamp: str
    processes: List[dict]        # [{name, pid, status}]
    connections: int             # total active connections
    public_ip: str
    process_names: List[str] = field(default_factory=list)

    def to_flat_row(self) -> dict:
        """Flatten for CSV output."""
        return {
            "timestamp": self.timestamp,
            "process_count": len(self.processes),
            "top_processes": "; ".join(self.process_names[:15]),
            "connection_count": self.connections,
            "public_ip": self.public_ip,
        }


def collect_processes() -> Tuple[List[dict], List[str]]:
    """Return running process info and name list."""
    procs = []
    names = []
    for p in psutil.process_iter(["pid", "name", "status"]):
        try:
            info = p.info
            procs.append(info)
            names.append(info["name"].lower())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return procs, names


def collect_connections() -> int:
    """Return count of active network connections."""
    try:
        return len(psutil.net_connections(kind="inet"))
    except psutil.AccessDenied:
        return -1  # signals access issue


def collect_public_ip() -> str:
    """Fetch public IP via a lightweight API. Fails gracefully."""
    try:
        resp = httpx.get("https://api.ipify.org", timeout=5)
        return resp.text.strip()
    except Exception:
        return "unavailable"


def take_snapshot() -> Snapshot:
    """Capture a full system snapshot."""
    procs, names = collect_processes()
    return Snapshot(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        processes=procs,
        connections=collect_connections(),
        public_ip=collect_public_ip(),
        process_names=names,
    )
