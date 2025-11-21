# Changelog

## Version 2.0 - Multi-Account Support

### 🎉 Major Changes

#### **Multi-Account System**
- ✅ Support for unlimited accounts
- ✅ Each account uses mobile number (for OTP login)
- ✅ Import/Export accounts via JSON
- ✅ Add accounts individually or in bulk
- ✅ Delete multiple accounts at once

#### **New Automation Tab**
- ✅ Separate page for automation control
- ✅ Three selection modes:
  - **Range**: Select accounts by range (1-10)
  - **Specific IDs**: Select specific accounts (1,3,5,7)
  - **All Accounts**: Run on all accounts
- ✅ Preview selection before running
- ✅ Headless mode checkbox moved here

#### **Updated Login Flow**
- ✅ Changed from email/password to mobile + OTP
- ✅ Opens Myntra login page (`myntra.com/login`)
- ✅ Browser stays open for manual OTP entry
- ✅ Processes multiple accounts sequentially

#### **UI Improvements**
- ✅ Account table with ID, Mobile, Name, Status
- ✅ Better button layout and organization
- ✅ Clear instructions and tooltips
- ✅ Real-time selection preview
- ✅ Enhanced logging for multi-account operations

### 📁 New Files
- `accounts.json` - Stores all accounts (auto-created)
- `accounts.example.json` - Example account format
- `FEATURES.md` - Detailed feature documentation
- `CHANGELOG.md` - This file

### 🔧 Technical Changes

#### **main.py**
- Restructured account management
- Added `create_automation_tab()` method
- Added account selection logic (range/specific/all)
- Added import/export functionality
- Added `refresh_accounts_list()` method
- Updated automation flow for multiple accounts

#### **myntra_automation.py**
- Changed from `email/password` to `mobile`
- Simplified to just open login page
- Removed complex login automation
- Browser stays open for manual interaction

### 🚀 Next Phase

The automation currently:
1. Opens Myntra login page
2. Displays mobile number
3. Waits for manual OTP entry

**Awaiting instructions for:**
- OTP automation (if needed)
- Product selection flow
- Cart operations
- Checkout automation
- Payment handling

### 📝 Migration Guide

If you have the old version:

1. **Old config format** (email/password) → **New format** (mobile numbers)
2. **Single account** → **Multiple accounts**
3. **Account tab** → Now for managing multiple accounts
4. **Automation settings** → Moved to dedicated Automation tab

### 🎯 How to Use v2.0

```bash
# Run the app
./run.sh

# Or manually
source venv/bin/activate
python main.py
```

**Workflow:**
1. Add accounts (Accounts tab)
2. Select accounts (Automation tab)  
3. Click Start Automation
4. Complete OTP for each account
5. Monitor in Logs tab

---

**Version 2.0 Ready! Waiting for next automation steps! 🚀**
