#!/bin/sh
set -e

# Soft check for database connection if DATABASE_URL is provided
if [ -n "$DATABASE_URL" ]; then
  echo "Checking database connection..."
  python << 'EOF'
import sys
import time
import os
from urllib.parse import urlparse
import socket

db_url = os.environ.get("DATABASE_URL", "")
if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
    parsed = urlparse(db_url)
    host = parsed.hostname
    port = parsed.port or 5432
    max_retries = 5
    connected = False
    for i in range(max_retries):
        try:
            with socket.create_connection((host, port), timeout=3):
                print(f"Database at {host}:{port} is reachable.")
                connected = True
                break
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            print(f"Database check retry... ({i+1}/{max_retries})")
            time.sleep(1)
    if not connected:
        print("Warning: Database check timed out during entrypoint startup. Proceeding with application boot...")
EOF
fi

# Run pending database migrations
if [ -f "alembic.ini" ]; then
  echo "Running database migrations with Alembic..."
  alembic upgrade head || echo "Alembic migration check complete."
fi

echo "Running development application..."
exec "$@"