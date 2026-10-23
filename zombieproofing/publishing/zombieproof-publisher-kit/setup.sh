#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
python3 -c 'import sys; assert sys.version_info >= (3, 12), "Python 3.12 or newer is required"'
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m playwright install chromium
echo 'Setup complete. Edit publishing-details.json and run ./build.sh.'
