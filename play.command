#!/bin/sh
# macOS double-click launcher: run the POSIX launcher beside this file.
set -eu
cd "$(dirname "$0")"
exec sh ./play.sh "$@"
