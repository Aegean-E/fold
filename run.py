#!/usr/bin/env python3
"""The user-facing entry point: `python run.py` starts Fold on port 8766."""

import sys

from fold.cli import main

if __name__ == "__main__":
    sys.exit(main())
