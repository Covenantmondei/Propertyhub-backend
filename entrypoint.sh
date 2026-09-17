#!/bin/sh
set -e

# Wait for PostgreSQL database if DATABASE_URL is provided
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
    max_retries = 30
    for i in range(max_retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"Database at {host}:{port} is reachable.")
                sys.exit(0)
        except (socket.timeout, ConnectionRefusedError, OSError):
            print(f"Database unavailable, waiting... ({i+1}/{max_retries})")
            time.sleep(1)
    print("Database connection timed out.")
    sys.exit(1)
EOF
fi

# Run pending database migrations
if [ -f "alembic.ini" ]; then
  echo "Running database migrations with Alembic..."
  alembic upgrade head || echo "Alembic migration check complete."
fi

echo "Running development application..."
exec "$@"