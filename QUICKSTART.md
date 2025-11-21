# Quick Start Guide

## ✅ All Fixed! Here's what was done:

### Issues Resolved:
1. ✅ **tkinter installed** - `python3-tk` system package
2. ✅ **rebrowser-playwright installed** - v1.52.0
3. ✅ **Chromium browser downloaded** - via rebrowser_playwright
4. ✅ **Import fixed** - Using `rebrowser_playwright.async_api`

## 🚀 Running the App

### Quick Run:
```bash
cd /home/watso/Vulncure/Project/myntra-tkinter
source venv/bin/activate
python main.py
```

### Or use the script:
```bash
./run.sh
```

## 📝 Usage Instructions

1. **Launch the app** - A GUI window will open
2. **Account Tab**:
   - Enter your Myntra email
   - Enter your password
   - Toggle headless mode (optional)

3. **Product Tab**:
   - Paste Myntra product URL
   - Enter size (M, L, XL, 42, etc.)

4. **Delivery Tab** (optional):
   - Fill in your delivery details
   - Will auto-fill during checkout

5. **Save Config**:
   - Click "💾 Save Config" button

6. **Start Automation**:
   - Click "🚀 Start Automation"
   - Watch progress in "📋 Logs" tab

## 🔧 Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install browser
python -m rebrowser_playwright install chromium

# Run the app
python main.py

# Deactivate virtual environment
deactivate
```

## ⚠️ Important Notes

- **Payment**: Automation stops at payment step - requires manual completion
- **Anti-detection**: rebrowser-playwright helps avoid bot detection
- **First run**: May be slower as browser downloads
- **Logs**: Check logs tab for detailed progress

## 🎯 What the App Does

1. Opens Myntra in automated browser
2. Logs into your account
3. Navigates to product page
4. Selects size
5. Adds to cart
6. Proceeds to checkout
7. Fills delivery details
8. **Stops at payment** (manual intervention required)

## 🐛 Troubleshooting

### App won't start
```bash
# Make sure you're in virtual environment
source venv/bin/activate
python main.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Browser not found
```bash
python -m rebrowser_playwright install chromium
```

## 📦 What's Installed

- **rebrowser-playwright**: 1.52.0 (includes anti-detection)
- **greenlet**: 3.2.4 (async support)
- **pyee**: 13.0.0 (event emitter)
- **Chromium browser**: v136 (automated browser)

---

**You're all set! Run `./run.sh` to start the app! 🎉**
