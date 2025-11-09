#!/bin/bash
# Project setup script

set -e

echo "Setting up Book Recommendation System..."
echo ""

# Install dependencies
echo "1. Installing dependencies with uv..."
uv sync --all-extras
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "2. Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠ Please edit .env with your API keys"
else
    echo "2. .env file already exists, skipping..."
fi
echo ""

# Start Redis
echo "3. Starting Redis with Docker Compose..."
docker-compose up -d redis
echo "✓ Redis started"
echo ""

echo "Setup complete! ✓"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your OpenAI API key"
echo "  2. Run 'uv run uvicorn src.main:app --reload' to start the dev server"
echo "  3. Visit http://localhost:8000/docs for API documentation"
