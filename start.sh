#!/bin/sh
# Alias for play.sh: start Fold and open its page.
set -eu
cd "$(dirname "$0")"
exec sh ./play.sh "$@"
