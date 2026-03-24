"""
test_collector.py — Unit tests for the data collector.
"""
import unittest
from agent.collector import collect_processes, collect_connections, take_snapshot


class TestCollector(unittest.TestCase):

    def test_collect_processes_returns_list(self):
        procs, names = collect_processes()
        self.assertIsInstance(procs, list)
        self.assertIsInstance(names, list)
        self.assertGreater(len(procs), 0, "Should have at least 1 process")

    def test_collect_connections_returns_int(self):
        count = collect_connections()
        self.assertIsInstance(count, int)

    def test_take_snapshot_structure(self):
        snap = take_snapshot()
        self.assertIsNotNone(snap.timestamp)
        self.assertIsInstance(snap.processes, list)
        self.assertIsInstance(snap.connections, int)
        self.assertIsInstance(snap.public_ip, str)

    def test_snapshot_to_flat_row(self):
        snap = take_snapshot()
        row = snap.to_flat_row()
        self.assertIn("timestamp", row)
        self.assertIn("process_count", row)
        self.assertIn("connection_count", row)
        self.assertIn("public_ip", row)


if __name__ == "__main__":
    unittest.main()
