#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python was not found on PATH."
  exit 1
fi

if [ ! -f "$PROJECT_ROOT/.venv/bin/python" ] && [ ! -f "$PROJECT_ROOT/.venv/Scripts/python.exe" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

if [ -f "$PROJECT_ROOT/.venv/bin/python" ]; then
  VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"
  VENV_PIP="$PROJECT_ROOT/.venv/bin/pip"
else
  VENV_PYTHON="$PROJECT_ROOT/.venv/Scripts/python.exe"
  VENV_PIP="$PROJECT_ROOT/.venv/Scripts/pip.exe"
fi

"$VENV_PIP" install --disable-pip-version-check -r requirements.txt

if ! "$VENV_PYTHON" -c "import importlib.util; raise SystemExit(0 if importlib.util.find_spec('en_core_web_sm') else 1)"; then
  "$VENV_PYTHON" -m spacy download en_core_web_sm
fi

"$VENV_PYTHON" main.py

REQUESTED_PORT="${STREAMLIT_PORT:-8501}"
STREAMLIT_PORT="$("$VENV_PYTHON" -c "
import socket
import sys

start_port = int(sys.argv[1])
for port in range(start_port, start_port + 25):
    sock = socket.socket()
    try:
        sock.bind(('0.0.0.0', port))
    except OSError:
        sock.close()
        continue
    sock.close()
    print(port)
    raise SystemExit(0)

raise SystemExit('No free Streamlit port found in the checked range.')
" "$REQUESTED_PORT")"

if [ "$STREAMLIT_PORT" != "$REQUESTED_PORT" ]; then
  echo "Port ${REQUESTED_PORT} was busy. Using http://localhost:${STREAMLIT_PORT} instead."
else
  echo "Starting dashboard at http://localhost:${STREAMLIT_PORT}"
fi

"$VENV_PYTHON" -m streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port "$STREAMLIT_PORT"
