#!/bin/sh
# One-click launcher for macOS and Linux: start Fold and open its page.
set -eu
cd "$(dirname "$0")"
exec python3 run.py --open "$@"
