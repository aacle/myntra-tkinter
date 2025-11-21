#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️ Virtual environment not found. Running setup first..."
    ./setup.sh
    source venv/bin/activate
fi

# Run the application
echo "🚀 Starting Myntra Automation App..."
python main.py
