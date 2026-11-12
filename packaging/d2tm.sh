#!/bin/sh
HERE="$(cd "$(dirname "$0")" && pwd)"
LD_LIBRARY_PATH="$HERE/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" exec "$HERE/d2tm" "$@"
