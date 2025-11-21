# Installation Guide

## Quick Fix for Setup Issues

### 1. Install tkinter (Required)

tkinter is a system package on Linux. Install it first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

### 2. Run Setup

After installing tkinter, run:

```bash
./setup.sh
```

This will:
- Check for Python 3 and tkinter
- Create a virtual environment
- Install playwright and rebrowser-playwright
- Install Playwright browsers

### 3. Run the Application

```bash
./run.sh
```

Or manually:
```bash
source venv/bin/activate
python main.py
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution:** Install python3-tk system package (see step 1 above)

### Issue: "rebrowser-playwright version not found"
**Solution:** Already fixed - now using version 1.52.0

### Issue: "playwright: command not found"
**Solution:** Run `source venv/bin/activate` before running playwright commands

## Manual Installation

If the automated setup doesn't work:

```bash
# 1. Install tkinter (system package)
sudo apt-get install python3-tk

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install Python packages
pip install -r requirements.txt

# 5. Install Playwright browsers
playwright install chromium

# 6. Run the application
python main.py
```
