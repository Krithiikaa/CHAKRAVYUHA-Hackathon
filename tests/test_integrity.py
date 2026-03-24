"""
test_integrity.py — Unit tests for SHA-256 integrity module.
"""
import unittest
import tempfile
from pathlib import Path
from agent.integrity import hash_file, write_checksums, verify_integrity


class TestIntegrity(unittest.TestCase):

    def test_hash_file_deterministic(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
            f.write(b"phantom agent test data")
            f.flush()
            path = Path(f.name)

        h1 = hash_file(path)
        h2 = hash_file(path)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)  # SHA-256 hex length
        path.unlink()

    def test_write_and_verify_checksums(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            d = Path(tmpdir)
            (d / "file1.txt").write_text("hello", encoding="utf-8")
            (d / "file2.txt").write_text("world", encoding="utf-8")

            write_checksums(d)
            results = verify_integrity(d)

            self.assertEqual(results["file1.txt"], "OK")
            self.assertEqual(results["file2.txt"], "OK")

    def test_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            d = Path(tmpdir)
            f = d / "secret.txt"
            f.write_text("original", encoding="utf-8")

            write_checksums(d)

            # Tamper with the file
            f.write_text("tampered!", encoding="utf-8")

            results = verify_integrity(d)
            self.assertEqual(results["secret.txt"], "TAMPERED")


if __name__ == "__main__":
    unittest.main()
