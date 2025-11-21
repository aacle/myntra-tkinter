"""
Myntra Order Placement Automation - Desktop Application
Main GUI application using tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
from datetime import datetime
from myntra_automation import MyntraAutomation


class MyntraAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Myntra Order Automation")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")
        
        # Configuration
        self.config_file = "config.json"
        self.accounts_file = "accounts.json"
        self.load_config()
        self.load_accounts()
        
        # Automation instance
        self.automation = None
        self.is_running = False
        
        # Selected accounts
        self.selected_accounts = []
        
        self.setup_ui()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "email": "",
                "password": "",
                "headless": False,
                "manual_otp": True,
                "browser_path": "",
                "product_url": "",
                "size": "",
                "pincode": "",
                "phone": "",
                "name": "",
                "address": "",
                "city": "",
                "state": ""
            }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_accounts(self):
        """Load accounts from accounts.json into self.accounts"""
        if os.path.exists(self.accounts_file):
            try:
                with open(self.accounts_file, 'r') as f:
                    data = json.load(f)
                    self.accounts = data if isinstance(data, list) else []
            except Exception:
                self.accounts = []
        else:
            self.accounts = []

    def save_accounts(self):
        """Persist self.accounts to accounts.json"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=4)
        except Exception as e:
            # Non-fatal; surface in logs if UI ready
            try:
                self.log_message(f"⚠️ Failed to save accounts: {e}")
            except Exception:
                pass

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#ff3f6c", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🛍️ Myntra Order Automation",
            font=("Arial", 24, "bold"),
            bg="#ff3f6c",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Account Tab
        self.create_account_tab()
        
        # Automation Tab
        self.create_automation_tab()
        
        # Product Tab
        self.create_product_tab()
        
        # Delivery Tab
        self.create_delivery_tab()
        
        # Logs Tab
        self.create_logs_tab()
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#f5f5f5")
        control_frame.pack(fill="x", padx=20, pady=10)
        
        self.start_button = tk.Button(
            control_frame,
            text="🚀 Start Automation",
            font=("Arial", 14, "bold"),
            bg="#03c04a",
            fg="white",
            padx=30,
            pady=10,
            command=self.start_automation,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
            text="⏹️ Stop",
            font=("Arial", 14, "bold"),
            bg="#ff3f6c",
            fg="white",
            padx=30,
            pady=10,
            command=self.stop_automation,
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        save_button = tk.Button(
            control_frame,
            text="💾 Save Config",
            font=("Arial", 14, "bold"),
            bg="#3466aa",
            fg="white",
            padx=30,
            pady=10,
            command=self.save_configuration,
            cursor="hand2"
        )
        save_button.pack(side="right", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#282c34",
            fg="white",
            font=("Arial", 10),
            anchor="w",
            padx=10,
            pady=5
        )
        status_bar.pack(fill="x", side="bottom")
    
    def create_account_tab(self):
        """Create accounts management tab"""
        account_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(account_frame, text="👤 Accounts")
        
        # Header with buttons
        header_frame = tk.Frame(account_frame, bg="white")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(
            header_frame,
            text="Manage Myntra Accounts",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(side="left")
        
        btn_frame = tk.Frame(header_frame, bg="white")
        btn_frame.pack(side="right")
        
        tk.Button(
            btn_frame,
            text="➕ Add Account",
            command=self.add_account_dialog,
            bg="#03c04a",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📥 Import",
            command=self.import_accounts,
            bg="#3466aa",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📤 Export",
            command=self.export_accounts,
            bg="#3466aa",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Delete",
            command=self.delete_selected_accounts,
            bg="#ff3f6c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        ).pack(side="left", padx=5)
        
        # Accounts list with scrollbar
        list_frame = tk.Frame(account_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview for accounts
        columns = ("ID", "Mobile", "Name", "Status")
        self.accounts_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=15)
        
        # Configure columns
        self.accounts_tree.column("#0", width=50, minwidth=50)
        self.accounts_tree.column("ID", width=80, minwidth=80)
        self.accounts_tree.column("Mobile", width=150, minwidth=150)
        self.accounts_tree.column("Name", width=200, minwidth=200)
        self.accounts_tree.column("Status", width=100, minwidth=100)
        
        # Configure headings
        self.accounts_tree.heading("#0", text="☑")
        self.accounts_tree.heading("ID", text="ID")
        self.accounts_tree.heading("Mobile", text="Mobile Number")
        self.accounts_tree.heading("Name", text="Name")
        self.accounts_tree.heading("Status", text="Status")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.accounts_tree.yview)
        self.accounts_tree.configure(yscrollcommand=scrollbar.set)
        
        self.accounts_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load accounts into tree
        self.refresh_accounts_list()
        
        # Info label
        info_label = tk.Label(
            account_frame,
            text="💡 Tip: Add multiple accounts and select them in the Automation tab",
            font=("Arial", 9),
            bg="white",
            fg="gray"
        )
        info_label.pack(pady=10)
    
    def create_automation_tab(self):
        """Create automation control tab"""
        automation_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(automation_frame, text="🚀 Automation")
        
        # Main container
        main_frame = tk.Frame(automation_frame, bg="white")
        main_frame.pack(pady=30, padx=30, fill="both", expand=True)
        
        tk.Label(
            main_frame,
            text="Automation Settings",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        # Account Selection Section
        selection_frame = tk.LabelFrame(main_frame, text="Account Selection", font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        selection_frame.pack(fill="x", pady=10)
        
        # Selection Mode
        tk.Label(selection_frame, text="Selection Mode:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        
        self.selection_mode = tk.StringVar(value="range")
        
        mode_frame = tk.Frame(selection_frame, bg="white")
        mode_frame.grid(row=0, column=1, sticky="w", pady=10)
        
        tk.Radiobutton(
            mode_frame,
            text="Range (e.g., 1-5)",
            variable=self.selection_mode,
            value="range",
            font=("Arial", 10),
            bg="white",
            command=self.update_selection_mode
        ).pack(side="left", padx=10)
        
        tk.Radiobutton(
            mode_frame,
            text="Specific IDs (e.g., 1,3,5)",
            variable=self.selection_mode,
            value="specific",
            font=("Arial", 10),
            bg="white",
            command=self.update_selection_mode
        ).pack(side="left", padx=10)
        
        tk.Radiobutton(
            mode_frame,
            text="All Accounts",
            variable=self.selection_mode,
            value="all",
            font=("Arial", 10),
            bg="white",
            command=self.update_selection_mode
        ).pack(side="left", padx=10)
        
        # Account input
        tk.Label(selection_frame, text="Account Selection:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        
        self.account_selection_entry = tk.Entry(selection_frame, font=("Arial", 12), width=40)
        self.account_selection_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        self.account_selection_entry.insert(0, "1-10")
        
        # Preview button
        tk.Button(
            selection_frame,
            text="Preview Selection",
            command=self.preview_selection,
            bg="#3466aa",
            fg="white",
            font=("Arial", 10),
            padx=15,
            pady=5
        ).grid(row=1, column=2, padx=10)
        
        # Selected accounts display
        self.selected_accounts_label = tk.Label(
            selection_frame,
            text="No accounts selected",
            font=("Arial", 10),
            bg="white",
            fg="gray"
        )
        self.selected_accounts_label.grid(row=2, column=1, sticky="w", pady=5)
        
        # Browser Settings Section
        browser_frame = tk.LabelFrame(main_frame, text="Browser Settings", font=("Arial", 12, "bold"), bg="white", padx=20, pady=15)
        browser_frame.pack(fill="x", pady=10)
        
        self.headless_var = tk.BooleanVar(value=self.config.get("headless", False))
        tk.Checkbutton(
            browser_frame,
            text="Headless Mode (Run browser in background)",
            variable=self.headless_var,
            font=("Arial", 11),
            bg="white"
        ).pack(anchor="w", pady=5)
        
        self.manual_otp_var = tk.BooleanVar(value=self.config.get("manual_otp", True))
        tk.Checkbutton(
            browser_frame,
            text="Manual OTP entry (keep browser open on OTP page)",
            variable=self.manual_otp_var,
            font=("Arial", 11),
            bg="white"
        ).pack(anchor="w", pady=5)

        # Browser Path Input
        tk.Label(browser_frame, text="Custom Browser Path (Optional):", font=("Arial", 11), bg="white").pack(anchor="w", pady=(10, 5))
        self.browser_path_entry = tk.Entry(browser_frame, font=("Arial", 10), width=50)
        self.browser_path_entry.pack(anchor="w", padx=5, pady=5)
        self.browser_path_entry.insert(0, self.config.get("browser_path", ""))
        
        tk.Label(
            browser_frame, 
            text="Leave empty to auto-detect. On Windows, point to chrome.exe if needed.", 
            font=("Arial", 9), 
            bg="white", 
            fg="gray"
        ).pack(anchor="w", padx=5)
        
        # Start Button
        start_frame = tk.Frame(main_frame, bg="white")
        start_frame.pack(pady=30)
        
        self.auto_start_button = tk.Button(
            start_frame,
            text="🚀 Start Automation",
            font=("Arial", 16, "bold"),
            bg="#03c04a",
            fg="white",
            padx=50,
            pady=15,
            command=self.start_automation,
            cursor="hand2"
        )
        self.auto_start_button.pack(side="left", padx=10)
        
        # Info Section
        info_frame = tk.Frame(main_frame, bg="#f0f0f0", relief="ridge", bd=2)
        info_frame.pack(fill="x", pady=20, padx=10)
        
        tk.Label(
            info_frame,
            text="ℹ️ How it works:",
            font=("Arial", 11, "bold"),
            bg="#f0f0f0"
        ).pack(anchor="w", padx=10, pady=5)
        
        tk.Label(
            info_frame,
            text="1. Select accounts using range (1-5) or specific IDs (1,3,5,7)",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#333"
        ).pack(anchor="w", padx=20, pady=2)
        
        tk.Label(
            info_frame,
            text="2. Click 'Preview Selection' to verify which accounts will be used",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#333"
        ).pack(anchor="w", padx=20, pady=2)
        
        tk.Label(
            info_frame,
            text="3. Click 'Start Automation' to begin the process",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#333"
        ).pack(anchor="w", padx=20, pady=2)
        
        tk.Label(
            info_frame,
            text="4. The automation will open Myntra login page for each account",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#333"
        ).pack(anchor="w", padx=20, pady=2)
    
    def create_product_tab(self):
        """Create product details tab"""
        product_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(product_frame, text="🛒 Product")
        
        form_frame = tk.Frame(product_frame, bg="white")
        form_frame.pack(pady=30, padx=30, fill="both", expand=True)
        
        tk.Label(
            form_frame,
            text="Product Information",
            font=("Arial", 16, "bold"),
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20, sticky="w")
        
        # Product URL
        tk.Label(form_frame, text="Product URL:", font=("Arial", 12), bg="white").grid(
            row=1, column=0, sticky="w", pady=10
        )
        self.product_url_entry = tk.Entry(form_frame, font=("Arial", 12), width=50)
        self.product_url_entry.grid(row=1, column=1, pady=10, padx=10)
        self.product_url_entry.insert(0, self.config.get("product_url", ""))
        
        # Size
        tk.Label(form_frame, text="Size:", font=("Arial", 12), bg="white").grid(
            row=2, column=0, sticky="w", pady=10
        )
        self.size_entry = tk.Entry(form_frame, font=("Arial", 12), width=50)
        self.size_entry.grid(row=2, column=1, pady=10, padx=10)
        self.size_entry.insert(0, self.config.get("size", ""))
        
        tk.Label(
            form_frame,
            text="(e.g., M, L, XL, 42, etc.)",
            font=("Arial", 9),
            bg="white",
            fg="gray"
        ).grid(row=3, column=1, sticky="w", padx=10)
    
    def create_delivery_tab(self):
        """Create delivery details tab"""
        delivery_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(delivery_frame, text="📦 Delivery")
        
        form_frame = tk.Frame(delivery_frame, bg="white")
        form_frame.pack(pady=30, padx=30, fill="both", expand=True)
        
        tk.Label(
            form_frame,
            text="Delivery Information",
            font=("Arial", 16, "bold"),
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20, sticky="w")
        
        fields = [
            ("Name:", "name"),
            ("Phone:", "phone"),
            ("Pincode:", "pincode"),
            ("Address:", "address"),
            ("City:", "city"),
            ("State:", "state")
        ]
        
        self.delivery_entries = {}
        for idx, (label, key) in enumerate(fields, start=1):
            tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(
                row=idx, column=0, sticky="w", pady=10
            )
            entry = tk.Entry(form_frame, font=("Arial", 12), width=50)
            entry.grid(row=idx, column=1, pady=10, padx=10)
            entry.insert(0, self.config.get(key, ""))
            self.delivery_entries[key] = entry
    
    def create_logs_tab(self):
        """Create logs tab"""
        logs_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(logs_frame, text="📋 Logs")
        
        tk.Label(
            logs_frame,
            text="Automation Logs",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            font=("Courier", 10),
            bg="#282c34",
            fg="#abb2bf",
            wrap=tk.WORD,
            height=20
        )
        self.logs_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Clear logs button
        clear_button = tk.Button(
            logs_frame,
            text="Clear Logs",
            command=self.clear_logs,
            bg="#ff3f6c",
            fg="white",
            font=("Arial", 10)
        )
        clear_button.pack(pady=10)
    
    def log_message(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        print(log_entry.strip())
    
    def clear_logs(self):
        """Clear all logs"""
        self.logs_text.delete(1.0, tk.END)
    
    def save_configuration(self):
        """Save current configuration"""
        self.config["headless"] = self.headless_var.get()
        self.config["manual_otp"] = self.manual_otp_var.get()
        self.config["browser_path"] = self.browser_path_entry.get().strip()
        self.config["product_url"] = self.product_url_entry.get().strip()
        self.config["size"] = self.size_entry.get()
        
        for key, entry in self.delivery_entries.items():
            self.config[key] = entry.get()
        
        self.save_config()
        self.log_message("✅ Configuration saved successfully")
        messagebox.showinfo("Success", "Configuration saved successfully!")
    
    def refresh_accounts_list(self):
        """Refresh the accounts tree view"""
        # Clear existing items
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        
        # Add accounts
        for idx, account in enumerate(self.accounts, start=1):
            self.accounts_tree.insert(
                "",
                "end",
                values=(
                    idx,
                    account.get("mobile", ""),
                    account.get("name", ""),
                    account.get("status", "Active")
                )
            )
    
    def add_account_dialog(self):
        """Show dialog to add new account"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Account")
        dialog.geometry("400x250")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Account", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
        
        form_frame = tk.Frame(dialog, bg="white")
        form_frame.pack(padx=30, pady=10)
        
        tk.Label(form_frame, text="Mobile Number:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", pady=10)
        mobile_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        mobile_entry.grid(row=0, column=1, pady=10)
        
        tk.Label(form_frame, text="Name (Optional):", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        name_entry.grid(row=1, column=1, pady=10)
        
        def save_account():
            mobile = mobile_entry.get().strip()
            if not mobile:
                messagebox.showerror("Error", "Please enter mobile number")
                return
            
            account = {
                "mobile": mobile,
                "name": name_entry.get().strip() or f"Account {len(self.accounts) + 1}",
                "status": "Active"
            }
            
            self.accounts.append(account)
            self.save_accounts()
            self.refresh_accounts_list()
            self.log_message(f"✅ Added account: {mobile}")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save", command=save_account, bg="#03c04a", fg="white", font=("Arial", 10), padx=20, pady=5).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, bg="#ff3f6c", fg="white", font=("Arial", 10), padx=20, pady=5).pack(side="left", padx=5)
    
    def import_accounts(self):
        """Import accounts from JSON file"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Import Accounts",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    imported = json.load(f)
                    if isinstance(imported, list):
                        self.accounts.extend(imported)
                        self.save_accounts()
                        self.refresh_accounts_list()
                        self.log_message(f"✅ Imported {len(imported)} accounts")
                        messagebox.showinfo("Success", f"Imported {len(imported)} accounts")
                    else:
                        messagebox.showerror("Error", "Invalid file format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def export_accounts(self):
        """Export accounts to JSON file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            title="Export Accounts",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.accounts, f, indent=4)
                self.log_message(f"✅ Exported {len(self.accounts)} accounts")
                messagebox.showinfo("Success", f"Exported {len(self.accounts)} accounts")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def delete_selected_accounts(self):
        """Delete selected accounts"""
        selected_items = self.accounts_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No accounts selected")
            return
        
        if messagebox.askyesno("Confirm", f"Delete {len(selected_items)} account(s)?"):
            # Get account IDs to delete
            ids_to_delete = []
            for item in selected_items:
                values = self.accounts_tree.item(item, "values")
                ids_to_delete.append(int(values[0]) - 1)  # Convert to 0-indexed
            
            # Delete in reverse order to maintain indices
            for idx in sorted(ids_to_delete, reverse=True):
                if 0 <= idx < len(self.accounts):
                    del self.accounts[idx]
            
            self.save_accounts()
            self.refresh_accounts_list()
            self.log_message(f"✅ Deleted {len(ids_to_delete)} account(s)")
    
    def update_selection_mode(self):
        """Update UI based on selection mode"""
        mode = self.selection_mode.get()
        if mode == "all":
            self.account_selection_entry.config(state="disabled")
            self.account_selection_entry.delete(0, tk.END)
            self.account_selection_entry.insert(0, "All accounts")
        else:
            self.account_selection_entry.config(state="normal")
            if mode == "range":
                self.account_selection_entry.delete(0, tk.END)
                self.account_selection_entry.insert(0, "1-10")
            else:
                self.account_selection_entry.delete(0, tk.END)
                self.account_selection_entry.insert(0, "1,2,3")
    
    def preview_selection(self):
        """Preview which accounts will be selected"""
        mode = self.selection_mode.get()
        selection_text = self.account_selection_entry.get().strip()
        
        try:
            selected_indices = []
            
            if mode == "all":
                selected_indices = list(range(len(self.accounts)))
            elif mode == "range":
                if "-" in selection_text:
                    start, end = map(int, selection_text.split("-"))
                    selected_indices = list(range(start - 1, min(end, len(self.accounts))))
                else:
                    messagebox.showerror("Error", "Invalid range format. Use: 1-5")
                    return
            elif mode == "specific":
                ids = [int(x.strip()) for x in selection_text.split(",")]
                selected_indices = [x - 1 for x in ids if 0 < x <= len(self.accounts)]
            
            if not selected_indices:
                messagebox.showwarning("Warning", "No accounts match the selection")
                return
            
            self.selected_accounts = [self.accounts[i] for i in selected_indices]
            
            # Update label
            account_names = [acc.get("name", acc.get("mobile")) for acc in self.selected_accounts[:5]]
            if len(self.selected_accounts) > 5:
                display_text = f"Selected {len(self.selected_accounts)} accounts: {', '.join(account_names[:3])}..."
            else:
                display_text = f"Selected {len(self.selected_accounts)} accounts: {', '.join(account_names)}"
            
            self.selected_accounts_label.config(text=display_text, fg="#03c04a")
            self.log_message(f"✅ Selected {len(self.selected_accounts)} accounts")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid selection: {str(e)}")
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.selected_accounts:
            messagebox.showerror("Error", "Please select accounts in Automation tab")
            return False
        return True
    
    def start_automation(self):
        """Start the automation process"""
        if not self.validate_inputs():
            return
        
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_var.set("Running...")
        
        # Save configuration before starting
        self.save_configuration()
        
        # Start automation in a separate thread
        thread = threading.Thread(target=self.run_automation)
        thread.daemon = True
        thread.start()
    
    def run_automation(self):
        """Run the automation process"""
        try:
            self.log_message("🚀 Starting Myntra automation...")
            self.log_message(f"📱 Processing {len(self.selected_accounts)} account(s)")
            
            for idx, account in enumerate(self.selected_accounts, start=1):
                if not self.is_running:
                    break
                
                self.log_message(f"\n{'='*50}")
                self.log_message(f"📱 Account {idx}/{len(self.selected_accounts)}: {account.get('name')} ({account.get('mobile')})")
                self.log_message(f"{'='*50}")
                
                self.automation = MyntraAutomation(
                    mobile=account.get("mobile"),
                    headless=self.headless_var.get(),
                    manual_otp=self.manual_otp_var.get(),
                    log_callback=self.log_message,
                    executable_path=self.config.get("browser_path", "")
                )
                
                # Just open Myntra login page for now
                success = self.automation.open_myntra_login()
                
                if success:
                    self.log_message(f"✅ Opened login page for {account.get('name')}")
                    self.log_message("⏸️ Waiting for further instructions...")
                else:
                    self.log_message(f"❌ Failed to open login for {account.get('name')}")
                
                # Cleanup after each account
                if self.automation:
                    self.automation.cleanup()
            
            self.log_message("\n✅ Automation completed!")
            self.status_var.set("Completed")
                
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            self.status_var.set("Error occurred")
        
        finally:
            self.is_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            if self.automation:
                self.automation.cleanup()
    
    def stop_automation(self):
        """Stop the automation process"""
        if self.automation:
            self.log_message("⏹️ Stopping automation...")
            self.automation.stop()
            self.is_running = False
            self.status_var.set("Stopped")
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")


def main():
    root = tk.Tk()
    app = MyntraAutomationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
