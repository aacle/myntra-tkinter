#!/bin/bash

echo "🚀 Setting up Myntra Automation Desktop App..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if tkinter is available
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "⚠️  tkinter is not installed"
    echo ""
    echo "Please install tkinter using:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    echo ""
    read -p "Press Enter after installing tkinter to continue..."
    
    # Check again
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "❌ tkinter still not found. Please install it and try again."
        exit 1
    fi
fi

echo "✅ tkinter found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
python -m rebrowser_playwright install chromium

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python main.py"
echo ""
echo "Or simply run: ./run.sh"
