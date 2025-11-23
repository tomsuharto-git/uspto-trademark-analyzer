#!/bin/bash
# Startup script for Railway deployment
# Sets up library paths for C++ dependencies

# Find and export gcc library path
GCC_LIB=$(find /nix/store -name "libstdc++.so.6" -type f 2>/dev/null | head -1 | xargs dirname)
if [ -n "$GCC_LIB" ]; then
    export LD_LIBRARY_PATH="$GCC_LIB:$LD_LIBRARY_PATH"
    echo "Set LD_LIBRARY_PATH to: $LD_LIBRARY_PATH"
else
    echo "Warning: Could not find libstdc++.so.6"
fi

# Start the application
cd backend && /opt/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT
