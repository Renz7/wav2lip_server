#!/usr/bin/env sh
echo "using $(python3 --version)"
echo "launch run.py with args '$*'"
if [ $# -lt 1 ]; then
    echo "run default command..."
    python3 run.py
fi
python3 run.py "$@"

