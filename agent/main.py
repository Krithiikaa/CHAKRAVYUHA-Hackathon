"""
main.py — Phantom Agent V1 Entry Point.
Consent gate → Scheduler loop → Collect → Detect → Alert.
"""

import sys
import time
import signal
import argparse

from agent.consent import request_consent
from agent.collector import take_snapshot
from agent.logger import write_snapshot, should_rotate, rotate_log
from agent.detector import analyse, simulate_login_failure
from agent.evidence import package_evidence
from agent.alerter import dispatch_alerts
from agent.integrity import verify_integrity
from agent.config import COLLECTION_INTERVAL, EVIDENCE_DIR


# ── Graceful shutdown ────────────────────────────────────
_running = True


def _shutdown(signum, frame):
    global _running
    print("\n[⏹] Shutdown signal received. Stopping agent…")
    _running = False


signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)


# ── Main Loop ────────────────────────────────────────────

def run_agent(demo_mode: bool = False):
    """Core agent loop."""
    print("=" * 60)
    print("  PHANTOM AGENT V1 — Ethical Forensic Monitor")
    print("=" * 60)

    # ── Consent Gate ──
    if not request_consent():
        sys.exit(0)

    print(f"[▶] Agent started | Interval: {COLLECTION_INTERVAL}s")
    print(f"[▶] Press Ctrl+C to stop\n")

    cycle = 0

    # If demo mode, simulate login failures to trigger an alert
    if demo_mode:
        print("[🎮] Demo mode active — simulating 3 failed logins…\n")
        for _ in range(3):
            simulate_login_failure()

    while _running:
        cycle += 1
        try:
            # ── 1. Collect ──
            snapshot = take_snapshot()
            print(
                f"[{cycle:>4}] {snapshot.timestamp} | "
                f"Procs: {len(snapshot.processes):>4} | "
                f"Conns: {snapshot.connections:>4} | "
                f"IP: {snapshot.public_ip}"
            )

            # ── 2. Log ──
            write_snapshot(snapshot)

            # ── 3. Rotate ──
            if should_rotate():
                archive = rotate_log()
                if archive:
                    print(f"[🔄] Log rotated → {archive.name}")

            # ── 4. Detect ──
            alerts = analyse(snapshot)

            # ── 5. Evidence + Alert ──
            if alerts:
                incident_dir = package_evidence(
                    alerts=alerts,
                    snapshot_data=snapshot.to_flat_row(),
                )
                dispatch_alerts(alerts, incident_dir)

            # ── 6. Wait ──
            time.sleep(COLLECTION_INTERVAL)

        except Exception as e:
            print(f"[✗] Error in cycle {cycle}: {e}")
            time.sleep(COLLECTION_INTERVAL)

    print("[✓] Agent stopped cleanly.")


# ── Verify Subcommand ────────────────────────────────────

def run_verify():
    """Verify integrity of all evidence folders."""
    print("=" * 60)
    print("  PHANTOM AGENT V1 — Evidence Integrity Check")
    print("=" * 60)

    if not EVIDENCE_DIR.exists():
        print("[!] No evidence directory found.")
        return

    incidents = sorted(EVIDENCE_DIR.iterdir())
    if not incidents:
        print("[!] No incidents found.")
        return

    for inc_dir in incidents:
        if not inc_dir.is_dir():
            continue
        print(f"\n📁 {inc_dir.name}")
        results = verify_integrity(inc_dir)
        for fname, status in results.items():
            icon = "✓" if status == "OK" else "✗"
            print(f"   [{icon}] {fname}: {status}")


# ── CLI ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Phantom Agent V1 — Ethical Forensic Monitor"
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # 'run' subcommand
    run_parser = sub.add_parser("run", help="Start the monitoring agent")
    run_parser.add_argument(
        "--demo", action="store_true",
        help="Run in demo mode (simulate threats)"
    )

    # 'verify' subcommand
    sub.add_parser("verify", help="Verify evidence integrity")

    args = parser.parse_args()

    if args.command == "run":
        run_agent(demo_mode=args.demo)
    elif args.command == "verify":
        run_verify()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
