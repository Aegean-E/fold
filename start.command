#!/bin/sh
# macOS double-click alias for play.command.
set -eu
cd "$(dirname "$0")"
exec sh ./play.sh "$@"
