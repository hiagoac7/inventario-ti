#!/usr/bin/env bash
# Build the Android app from the exact source checked out from GitHub.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/app-android"
python3 -m pip install --upgrade --break-system-packages "Cython==0.29.36" buildozer virtualenv || python3 -m pip install --upgrade "Cython==0.29.36" buildozer virtualenv
yes | buildozer -v android debug
echo "APK files:"
find bin -maxdepth 1 -name '*.apk' -type f -print
