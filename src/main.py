# -*- coding: utf-8 -*-
"""Windows 11 Security Hardener v2.0"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import winreg
import os
import sys
import ctypes
from datetime import datetime

class SecurityHardener:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows 11 Security Hardener v2.0")
        self.root.geometry("900x700")
        
        if not self.is_admin():
            messagebox.showerror("Error", "Must run as administrator!")
            sys.exit(1)
        
        self.log_dir = r"C:\ProgramData\WinSecHardener"
        self.log_file = os.path.join(self.log_dir, "audit.log")
        os.makedirs(self.log_dir, exist_ok=True)
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Windows 11 Security Hardener", font=('Segoe UI', 16, 'bold')).pack(pady=(0, 10))
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.system_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.system_frame, text="System")
        
        self.apps_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.apps_frame, text="Apps")
        
        self.usb_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.usb_frame, text="USB/Network")
        
        self.browser_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.browser_frame, text="Browser")
        
        self.log_frame = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.log_frame, text="Log")
        
        self.create_system_tab()
        self.create_apps_tab()
        self.create_usb_tab()
        self.create_browser_tab()
        self.create_log_tab()
        
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        ttk.Button(action_frame, text="Apply All", command=self.apply_all_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Reset All", command=self.reset_all_settings).pack(side=tk.LEFT, padx=5)
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(action_frame, textvariable=self.status_var, foreground="green").pack(side=tk.RIGHT, padx=10)
        
        self.init_variables()
        self.log_event("Application started")
    
    def init_variables(self):
        self.var_regedit = tk.BooleanVar()
        self.var_cmd = tk.BooleanVar()
        self.var_powershell = tk.BooleanVar()
        self.var_taskmgr = tk.BooleanVar()
        self.var_controlpanel = tk.BooleanVar()
        self.var_settings = tk.BooleanVar()
        self.var_winr = tk.BooleanVar()
        self.var_block_games = tk.BooleanVar()
        self.var_block_temp = tk.BooleanVar()
        self.var_usb_readonly = tk.BooleanVar()
        self.var_usb_disable = tk.BooleanVar()
        self.var_network_restrict = tk.BooleanVar()
        self.var_browser_extensions = tk.BooleanVar()
        self.var_browser_devtools = tk.BooleanVar()
        self.var_browser_passwords = tk.BooleanVar()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def log_event(self, msg):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
        except:
            pass
    
    def set_reg(self, path, name, val, root=winreg.HKEY_CURRENT_USER):
        try:
            key = winreg.CreateKeyEx(root, path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)
            winreg.CloseKey(key)
        except:
            pass
    
    def create_system_tab(self):
        grp = ttk.LabelFrame(self.system_frame, text="System Component Blocking", padding="10")
        grp.pack(fill=tk.X, pady=5)
        items = [
            ("Block RegEdit", self.var_regedit),
            ("Block CMD", self.var_cmd),
            ("Block PowerShell", self.var_powershell),
            ("Block Task Manager", self.var_taskmgr),
            ("Block Control Panel", self.var_controlpanel),
            ("Block Settings App", self.var_settings),
            ("Disable Win+R", self.var_winr),
        ]
        for txt, var in items:
            ttk.Checkbutton(grp, text=txt, variable=var).pack(anchor=tk.W, pady=2)
    
    def create_apps_tab(self):
        grp = ttk.LabelFrame(self.apps_frame, text="Gaming Platforms", padding="10")
        grp.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(grp, text="Block Steam, Epic Games", variable=self.var_block_games).pack(anchor=tk.W)
        grp2 = ttk.LabelFrame(self.apps_frame, text="Temporary Folders", padding="10")
        grp2.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(grp2, text="Block execution from %TEMP%", variable=self.var_block_temp).pack(anchor=tk.W)
        bl_grp = ttk.LabelFrame(self.apps_frame, text="Application Blacklist (.exe)", padding="10")
        bl_grp.pack(fill=tk.BOTH, expand=True, pady=5)
        self.blacklist_listbox = tk.Listbox(bl_grp, height=6)
        self.blacklist_listbox.pack(fill=tk.BOTH, expand=True)
        btn_fr = ttk.Frame(bl_grp)
        btn_fr.pack(fill=tk.X, pady=5)
        self.blacklist_entry = ttk.Entry(btn_fr, width=40)
        self.blacklist_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_fr, text="Add", command=lambda: self.blacklist_listbox.insert(tk.END, self.blacklist_entry.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_fr, text="Remove", command=lambda: self.blacklist_listbox.delete(tk.ACTIVE)).pack(side=tk.LEFT, padx=5)
    
    def create_usb_tab(self):
        grp = ttk.LabelFrame(self.usb_frame, text="USB Restrictions", padding="10")
        grp.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(grp, text="USB Read-Only Mode", variable=self.var_usb_readonly).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(grp, text="Disable USB Ports", variable=self.var_usb_disable).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(grp, text="Network Restrictions", variable=self.var_network_restrict).pack(anchor=tk.W, pady=2)
    
    def create_browser_tab(self):
        grp = ttk.LabelFrame(self.browser_frame, text="Browser Restrictions (Chrome/Edge)", padding="10")
        grp.pack(fill=tk.BOTH, expand=True, pady=5)
        items = [
            ("Block Extensions", self.var_browser_extensions),
            ("Block DevTools (F12)", self.var_browser_devtools),
            ("Disable Password Save", self.var_browser_passwords),
        ]
        for txt, var in items:
            ttk.Checkbutton(grp, text=txt, variable=var).pack(anchor=tk.W, pady=3)
    
    def create_log_tab(self):
        grp = ttk.LabelFrame(self.log_frame, text="Event Log", padding="10")
        grp.pack(fill=tk.BOTH, expand=True)
        self.log_text = scrolledtext.ScrolledText(grp, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        ttk.Button(grp, text="Refresh", command=self.refresh_log).pack(pady=5)
        self.refresh_log()
    
    def refresh_log(self):
        self.log_text.delete(1.0, tk.END)
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, "r", encoding="utf-8") as f:
                    self.log_text.insert(tk.END, f.read())
        except:
            pass
    
    def apply_all_settings(self):
        if not messagebox.askyesno("Confirm", "Apply all selected settings?"):
            return
        cnt = 0
        if self.var_regedit.get():
            self.set_reg(r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableRegistryTools", 1)
            cnt += 1
        if self.var_cmd.get():
            self.set_reg(r"Software\Policies\Microsoft\Windows\System", "DisableCMD", 2)
            cnt += 1
        if self.var_powershell.get():
            self.set_reg(r"Software\Policies\Microsoft\PowerShell", "EnableScripts", 0)
            cnt += 1
        if self.var_taskmgr.get():
            self.set_reg(r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "DisableTaskMgr", 1)
            cnt += 1
        if self.var_controlpanel.get():
            self.set_reg(r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoControlPanel", 1)
            cnt += 1
        if self.var_settings.get():
            self.set_reg(r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoSetFolders", 1)
            cnt += 1
        if self.var_winr.get():
            self.set_reg(r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "NoRun", 1)
            cnt += 1
        if self.var_usb_readonly.get():
            self.set_reg(r"SYSTEM\CurrentControlSet\Control\StorageDevicePolicies", "WriteProtect", 1, winreg.HKEY_LOCAL_MACHINE)
            cnt += 1
        if self.var_usb_disable.get():
            self.set_reg(r"SYSTEM\CurrentControlSet\Services\USBSTOR", "Start", 4, winreg.HKEY_LOCAL_MACHINE)
            cnt += 1
        if self.var_browser_extensions.get():
            self.set_reg(r"Software\Policies\Google\Chrome", "ExtensionInstallBlocklist", "*")
            cnt += 1
        if self.var_browser_devtools.get():
            self.set_reg(r"Software\Policies\Google\Chrome", "DeveloperToolsAvailability", 2)
            cnt += 1
        if self.var_browser_passwords.get():
            self.set_reg(r"Software\Policies\Google\Chrome", "PasswordManagerEnabled", 0)
            cnt += 1
        self.log_event(f"Applied {cnt} settings")
        self.status_var.set(f"Applied {cnt} settings")
        messagebox.showinfo("Done", f"Applied {cnt} settings!")
        self.refresh_log()
    
    def reset_all_settings(self):
        if not messagebox.askyesno("Confirm", "Reset ALL settings?"):
            return
        paths = [
            r"Software\Microsoft\Windows\CurrentVersion\Policies\System",
            r"Software\Policies\Microsoft\Windows\System",
            r"Software\Policies\Microsoft\PowerShell",
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer",
            r"Software\Policies\Google\Chrome",
        ]
        for p in paths:
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, p)
            except:
                pass
        self.init_variables()
        self.log_event("Settings reset")
        self.status_var.set("Reset")
        messagebox.showinfo("Done", "Settings reset to default!")
        self.refresh_log()

def main():
    root = tk.Tk()
    SecurityHardener(root)
    root.mainloop()

if __name__ == "__main__":
    main()
