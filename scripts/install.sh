#!/usr/bin/env bash
# ============================================================================
# ~/git/dotfiles/scripts/install.sh - Bootstrap wrapper for 'aco'
# Running './scripts/install.sh' with no arguments runs 'aco install'.
# All other arguments are forwarded directly to '~/git/dotfiles/scripts/aco'.
# ============================================================================
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPTS_DIR="$(dirname "$SCRIPT_PATH")"

if [[ $# -eq 0 ]]; then
    exec "$SCRIPTS_DIR/aco" install
else
    exec "$SCRIPTS_DIR/aco" "$@"
fi
