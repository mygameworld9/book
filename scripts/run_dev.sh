#!/bin/bash
# Development server startup script

set -e

echo "Starting development server..."
echo "Make sure Redis is running: docker-compose up -d redis"
echo ""

# Start uvicorn with hot reload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
