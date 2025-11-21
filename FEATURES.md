# 🎉 New Features - Multi-Account Myntra Automation

## ✨ What's New

### 1. **Multi-Account Support**
- Add unlimited Myntra accounts
- Each account stored with mobile number (for OTP login)
- Import/Export accounts in bulk via JSON files

### 2. **Flexible Account Selection**
- **Range Mode**: Select accounts 1-10, 5-20, etc.
- **Specific IDs**: Select specific accounts like 1,3,5,7,9
- **All Accounts**: Run automation on all added accounts

### 3. **Separate Automation Page**
- Dedicated automation control interface
- Preview selected accounts before starting
- Headless mode toggle for convenience
- Clear instructions and status

### 4. **Mobile + OTP Login**
- Changed from email/password to mobile + OTP
- Aligns with Myntra's actual login flow
- Browser stays open for manual OTP entry

## 📚 How to Use

### **Step 1: Add Accounts**

#### Option A: Add Single Account
1. Go to **👤 Accounts** tab
2. Click **➕ Add Account**
3. Enter mobile number (e.g., 9876543210)
4. Enter name (optional)
5. Click **Save**

#### Option B: Import Multiple Accounts
1. Create a JSON file with this format:
```json
[
    {
        "mobile": "9876543210",
        "name": "Account 1",
        "status": "Active"
    },
    {
        "mobile": "9876543211",
        "name": "Account 2",
        "status": "Active"
    }
]
```
2. Click **📥 Import** button
3. Select your JSON file
4. All accounts will be imported

### **Step 2: Select Accounts for Automation**

1. Go to **🚀 Automation** tab
2. Choose selection mode:
   - **Range**: Enter "1-5" to select accounts 1 through 5
   - **Specific IDs**: Enter "1,3,5" to select specific accounts
   - **All Accounts**: Automatically selects all

3. Click **Preview Selection** to verify
4. You'll see which accounts are selected

### **Step 3: Configure Browser**

- Check **Headless Mode** if you want browser to run in background
- Uncheck to see the browser (recommended for first time)

### **Step 4: Start Automation**

1. Click **🚀 Start Automation**
2. The app will process each selected account
3. For each account:
   - Opens Myntra login page
   - Shows mobile number
   - Waits for you to complete OTP login
4. Monitor progress in **📋 Logs** tab

## 🎯 Current Functionality

Right now, the automation:
- ✅ Opens Myntra login page
- ✅ Displays mobile number for reference
- ✅ Keeps browser open for manual OTP entry
- ⏸️ Waits for further instructions

## 📋 Accounts Management

### **View Accounts**
- All accounts shown in a table
- Displays: ID, Mobile Number, Name, Status

### **Delete Accounts**
1. Select accounts in the list (click to select)
2. Click **🗑️ Delete** button
3. Confirm deletion

### **Export Accounts**
1. Click **📤 Export** button
2. Choose location to save JSON file
3. All accounts exported for backup

## 🔧 Technical Details

### File Structure
```
myntra-tkinter/
├── main.py                 # GUI with multi-account support
├── myntra_automation.py    # Simplified to open login only
├── accounts.json           # Your accounts (auto-saved)
├── accounts.example.json   # Example account format
├── config.json            # App configuration
└── requirements.txt       # Dependencies
```

### Data Format

**accounts.json**:
```json
[
    {
        "mobile": "9876543210",
        "name": "My Primary Account",
        "status": "Active"
    }
]
```

**config.json**:
```json
{
    "headless": false,
    "product_url": "",
    "size": "",
    "pincode": "",
    "phone": "",
    "name": "",
    "address": "",
    "city": "",
    "state": ""
}
```

## 🚀 Quick Workflow

1. **Add 10 accounts** via Import
2. **Go to Automation tab**
3. **Select accounts 1-5**
4. **Click Preview** → See 5 accounts selected
5. **Click Start** → Opens login for each
6. **Complete OTP** for each account
7. **Monitor logs** for progress

## 📊 Selection Examples

### Range Selection
- `1-10` → Selects accounts 1 through 10
- `5-15` → Selects accounts 5 through 15
- `1-100` → Selects accounts 1 through 100 (or max available)

### Specific Selection
- `1,5,10` → Selects accounts 1, 5, and 10
- `2,4,6,8,10` → Selects even-numbered accounts
- `1,3,5,7,9` → Selects odd-numbered accounts

### All Selection
- Automatically includes every account in your list
- No manual entry needed

## ⚠️ Important Notes

1. **Mobile Number Format**: Enter without country code (e.g., 9876543210)
2. **OTP Login**: You must manually enter OTP - automation waits
3. **Browser Timeout**: Browser stays open for 5 minutes per account
4. **Stop Button**: Use to stop automation at any time
5. **Logs Tab**: Monitor all activity and errors

## 🔜 Next Steps

The automation currently opens login pages. You'll provide further instructions for:
- OTP handling
- Product selection
- Cart management
- Checkout process
- Payment flow

## 💡 Tips

- **Start Small**: Test with 1-2 accounts first
- **Use Names**: Give accounts meaningful names for easy identification
- **Regular Backups**: Export accounts regularly
- **Watch Logs**: Always monitor the Logs tab during automation
- **Headless Later**: Use visible browser first, then enable headless mode

---

**Ready to automate! Add your accounts and let me know the next steps! 🎯**
