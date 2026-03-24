"""
integrity.py — SHA-256 hashing and tamper verification.
Every evidence file is hashed; checksums are stored alongside.
"""

import hashlib
from pathlib import Path
from typing import Dict


def hash_file(filepath: Path) -> str:
    """Compute SHA-256 hex digest of a file."""
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def hash_directory(directory: Path) -> Dict[str, str]:
    """Hash every file in a directory. Returns {filename: hash}."""
    checksums = {}
    for item in sorted(directory.iterdir()):
        if item.is_file() and item.name != "checksums.sha256":
            checksums[item.name] = hash_file(item)
    return checksums


def write_checksums(directory: Path) -> Path:
    """Generate and write a checksums.sha256 file."""
    checksums = hash_directory(directory)
    checksum_file = directory / "checksums.sha256"
    lines = [f"{h}  {name}" for name, h in checksums.items()]
    checksum_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return checksum_file


def verify_integrity(directory: Path) -> Dict[str, str]:
    """
    Verify all files against stored checksums.
    Returns dict of {filename: status} where status is
    'OK', 'TAMPERED', or 'MISSING'.
    """
    checksum_file = directory / "checksums.sha256"
    if not checksum_file.exists():
        return {"_error": "No checksums.sha256 found"}

    stored: Dict[str, str] = {}
    for line in checksum_file.read_text(encoding="utf-8").strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) == 2:
            stored[parts[1]] = parts[0]

    results: Dict[str, str] = {}
    for name, expected_hash in stored.items():
        fpath = directory / name
        if not fpath.exists():
            results[name] = "MISSING"
        else:
            actual = hash_file(fpath)
            results[name] = "OK" if actual == expected_hash else "TAMPERED"

    return results
