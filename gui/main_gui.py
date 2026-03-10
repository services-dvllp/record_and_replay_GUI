"""Compatibility entry-point for legacy GUI without changing layout."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "Record_and_Replay_v1.69.py"), run_name="__main__")
