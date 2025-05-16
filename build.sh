#!/bin/bash
echo "Starting local build process..."
set -e # Exit immediately if a command exits with a non-zero status.

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
fi

source venv/bin/activate
echo "Virtual environment activated."

# Upgrade pip and install requirements
echo "Installing dependencies..."
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories (if not handled by app logic on startup)
mkdir -p app/static/pdfs
mkdir -p output/pdfs

echo "Local build setup completed successfully!"
echo "To run locally (after activating venv):"
echo "Ensure your .env file is configured, then run:"
echo "uvicorn app.main:app --reload --port 8000" 