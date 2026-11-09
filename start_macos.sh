#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -x .venv/bin/python ]]; then
    echo "[SETUP] Creating Python environment and installing pyserial..."
    python3 -m venv .venv
    .venv/bin/python -m pip install pyserial
fi

if [[ "${1:-}" == "list" ]]; then
    exec .venv/bin/python record_ppg.py --list-ports
fi

if [[ -z "${1:-}" ]]; then
    echo "Usage: bash start_macos.sh list"
    echo "       bash start_macos.sh /dev/cu.usbserial-110 [seconds]"
    echo "Example: bash start_macos.sh /dev/cu.usbserial-110 30"
    exit 1
fi

if [[ -z "${2:-}" ]]; then
    exec .venv/bin/python record_ppg.py --port "$1"
else
    exec .venv/bin/python record_ppg.py --port "$1" --seconds "$2"
fi
