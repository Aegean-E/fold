"""Allow `python -m fold` as the same entry point as `python run.py`."""

import sys

from fold.cli import main

if __name__ == "__main__":
    sys.exit(main())
