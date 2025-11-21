# Myntra Order Automation Desktop App

A desktop application built with **tkinter** and **rebrowser-playwright** for automating order placement on Myntra ecommerce platform.

## 🚀 Features

- **Modern GUI Interface**: Clean and intuitive tkinter-based desktop application
- **Browser Automation**: Powered by rebrowser-playwright for reliable automation
- **Account Management**: Save and manage Myntra account credentials
- **Product Selection**: Easy product URL and size configuration
- **Delivery Management**: Store and auto-fill delivery information
- **Real-time Logs**: Monitor automation progress with detailed logs
- **Configuration Persistence**: Save settings for future use

## 📋 Requirements

- Python 3.8 or higher
- tkinter (usually comes with Python)
- playwright
- rebrowser-playwright

## 🔧 Installation

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Playwright browsers**:
```bash
playwright install chromium
```

## 🎯 Usage

1. **Run the application**:
```bash
python main.py
```

2. **Configure Account Settings**:
   - Navigate to the **Account** tab
   - Enter your Myntra email and password
   - Toggle headless mode if you want browser to run in background

3. **Set Product Details**:
   - Go to the **Product** tab
   - Paste the Myntra product URL
   - Specify the desired size (e.g., M, L, XL, 42)

4. **Add Delivery Information** (Optional):
   - Switch to the **Delivery** tab
   - Fill in your delivery details
   - These will be auto-filled during checkout

5. **Save Configuration**:
   - Click the **Save Config** button to persist your settings

6. **Start Automation**:
   - Click **Start Automation** button
   - Monitor progress in the **Logs** tab
   - The automation will handle login, product selection, and adding to cart

## 📁 Project Structure

```
myntra-tkinter/
├── main.py                 # Main GUI application
├── myntra_automation.py    # Automation logic with playwright
├── requirements.txt        # Python dependencies
├── config.json            # User configuration (auto-generated)
└── README.md              # Documentation
```

## ⚙️ Configuration

The application saves configuration in `config.json`. This includes:
- Account credentials
- Product preferences
- Delivery information
- Browser settings

## 🔒 Security Notes

- Store credentials securely
- The `config.json` file contains sensitive information
- Use at your own risk and comply with Myntra's terms of service
- Payment step requires manual intervention for security

## ⚠️ Important Notes

1. **Anti-bot Detection**: rebrowser-playwright helps avoid detection, but Myntra may still detect automation
2. **Payment**: The automation stops at payment stage for security - manual intervention required
3. **Rate Limiting**: Don't run too frequently to avoid being blocked
4. **Terms of Service**: Ensure you comply with Myntra's terms of service

## 🛠️ Troubleshooting

### Browser doesn't launch
- Run: `playwright install chromium`
- Check if Chrome/Chromium is installed

### Login fails
- Verify credentials are correct
- Try running in non-headless mode to see what's happening
- Myntra may require OTP verification

### Size not found
- Ensure size format matches Myntra's display (case-sensitive)
- Check if product is in stock

### Automation stops unexpectedly
- Check logs tab for error messages
- Website structure may have changed
- Try disabling headless mode to debug

## 📝 Development

To modify or extend the automation:

1. **GUI Changes**: Edit `main.py`
2. **Automation Logic**: Modify `myntra_automation.py`
3. **Add Features**: Update both files and maintain separation of concerns

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is for educational purposes only. Use responsibly and at your own risk.

## ⚡ Quick Start Example

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run the application
python main.py
```

Then:
1. Fill in your Myntra credentials
2. Add product URL and size
3. Click "Start Automation"
4. Monitor logs for progress

## 🎨 UI Preview

The application features:
- **Header**: Myntra-themed pink header with app title
- **Tabbed Interface**: Organized into Account, Product, Delivery, and Logs
- **Control Buttons**: Start, Stop, and Save Configuration
- **Status Bar**: Real-time status updates
- **Modern Design**: Clean, professional appearance

## 📞 Support

For issues or questions:
- Check the logs tab for detailed error messages
- Ensure all dependencies are installed
- Verify Myntra website is accessible

---

**Disclaimer**: This tool is for educational purposes. Automated interactions with websites may violate terms of service. Use responsibly and ethically.
