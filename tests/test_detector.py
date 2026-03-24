"""
test_detector.py — Unit tests for the anomaly detector.
"""
import unittest
from agent.collector import Snapshot
from agent.detector import analyse, simulate_login_failure, reset_login_failures, _process_history


class TestDetector(unittest.TestCase):

    def setUp(self):
        _process_history.clear()
        reset_login_failures()

    def test_no_alerts_on_clean_snapshot(self):
        snap = Snapshot(
            timestamp="2026-03-24T12:00:00Z",
            processes=[{"name": "python", "pid": 1, "status": "running"}],
            connections=5,
            public_ip="1.2.3.4",
            process_names=["python"],
        )
        alerts = analyse(snap)
        self.assertEqual(len(alerts), 0)

    def test_high_connection_alert(self):
        snap = Snapshot(
            timestamp="2026-03-24T12:00:00Z",
            processes=[],
            connections=100,
            public_ip="1.2.3.4",
            process_names=[],
        )
        alerts = analyse(snap)
        rules = [a.rule for a in alerts]
        self.assertIn("HIGH_CONNECTION_COUNT", rules)

    def test_login_failure_alert(self):
        for _ in range(3):
            simulate_login_failure()
        snap = Snapshot(
            timestamp="2026-03-24T12:00:00Z",
            processes=[],
            connections=1,
            public_ip="1.2.3.4",
            process_names=[],
        )
        alerts = analyse(snap)
        rules = [a.rule for a in alerts]
        self.assertIn("MULTIPLE_LOGIN_FAILURES", rules)


if __name__ == "__main__":
    unittest.main()
