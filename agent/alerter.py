"""
alerter.py — Multi-channel alert system.
OS notification + SMTP email + REST webhook to MERN backend.
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List

import httpx
from plyer import notification

from agent.config import (
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS,
    ALERT_RECIPIENT, API_BASE_URL, DASHBOARD_URL,
)
from agent.detector import ThreatAlert


# ═════════════════════════════════════════════════════════
#  OS-Level Toast Notification
# ═════════════════════════════════════════════════════════

def send_os_notification(alerts: List[ThreatAlert]):
    """Fire an OS-level toast notification."""
    top = alerts[0]
    try:
        notification.notify(
            title=f"⚠ Phantom Agent — {top.severity} Alert",
            message=f"{top.description}\n\nDashboard → {DASHBOARD_URL}",
            app_name="Phantom Agent V1",
            timeout=10,
        )
    except Exception as e:
        print(f"[⚠] OS notification failed: {e}")


# ═════════════════════════════════════════════════════════
#  SMTP Email Alert
# ═════════════════════════════════════════════════════════

def send_email_alert(alerts: List[ThreatAlert], incident_dir: Path):
    """Send an email alert via SMTP. Credentials from .env only."""
    if not SMTP_USER or not SMTP_PASS:
        print("[⚠] SMTP not configured — skipping email alert.")
        return

    subject = f"[Phantom Agent] {alerts[0].severity} — {alerts[0].rule}"

    body_lines = [
        "🔒 Phantom Agent V1 — Threat Alert",
        "=" * 50,
        "",
    ]
    for a in alerts:
        body_lines.extend([
            f"Rule     : {a.rule}",
            f"Severity : {a.severity}",
            f"Detail   : {a.description}",
            f"Time     : {a.timestamp}",
            "-" * 40,
        ])
    body_lines.extend([
        "",
        f"Evidence  : {incident_dir}",
        f"Dashboard : {DASHBOARD_URL}",
        "",
        "— Phantom Agent V1 (automated)",
    ])

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_RECIPIENT
    msg["Subject"] = subject
    msg.attach(MIMEText("\n".join(body_lines), "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("[📧] Email alert sent.")
    except Exception as e:
        print(f"[⚠] Email alert failed: {e}")


# ═════════════════════════════════════════════════════════
#  REST API Webhook (MERN Backend)
# ═════════════════════════════════════════════════════════

def send_webhook(alerts: List[ThreatAlert], incident_dir: Path):
    """POST alert payload to the MERN backend API."""
    payload = {
        "incident_id": incident_dir.name,
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
        "evidence_path": str(incident_dir),
        "dashboard_url": DASHBOARD_URL,
    }

    try:
        resp = httpx.post(
            f"{API_BASE_URL}/alerts",
            json=payload,
            timeout=10,
        )
        print(f"[🌐] Webhook sent → {resp.status_code}")
    except Exception as e:
        print(f"[⚠] Webhook failed: {e}")


# ═════════════════════════════════════════════════════════
#  Unified Alert Dispatcher
# ═════════════════════════════════════════════════════════

def dispatch_alerts(alerts: List[ThreatAlert], incident_dir: Path):
    """Fire all alert channels in sequence."""
    if not alerts:
        return

    print(f"\n[🚨] {len(alerts)} threat(s) detected! Dispatching alerts…")
    send_os_notification(alerts)
    send_email_alert(alerts, incident_dir)
    send_webhook(alerts, incident_dir)
