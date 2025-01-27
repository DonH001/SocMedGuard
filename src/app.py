import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import win32gui
import win32process
import subprocess
from plyer import notification
from config.app_config import APPS_CONFIG, COOLDOWN_PERIOD, HOSTS_PATH, REDIRECT_IP, SETTINGS_FILE

class SocialMediaBlocker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Social Media Timer & Blocker")
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Set window dimensions and calculate center position
        window_width = 600
        window_height = 800
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        self.window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        
        # Make window responsive
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.window.configure(bg='#f0f0f0')
        self.hosts_path = HOSTS_PATH
        self.redirect = REDIRECT_IP
        self.cooldown_period = COOLDOWN_PERIOD
        
        self.apps = self._initialize_apps()
        self.load_settings()
        self.setup_gui()
        self.start_monitoring()

    def _initialize_apps(self):
        apps = {}
        for app_name, config in APPS_CONFIG.items():
            apps[app_name] = {
                **config,
                "time_remaining": 0,
                "is_running": False,
                "is_blocked": False,
                "allowed_time": 0,
                "cooldown_until": 0
            }
        return apps

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as file:
                settings = json.load(file)
                for app_name, app_data in settings.items():
                    if app_name in self.apps:
                        self.apps[app_name].update(app_data)

    def save_settings(self):
        settings = {app_name: {
            "time_remaining": app_data["time_remaining"],
            "is_running": app_data["is_running"],
            "is_blocked": app_data["is_blocked"],
            "allowed_time": app_data["allowed_time"],
            "cooldown_until": app_data["cooldown_until"]
        } for app_name, app_data in self.apps.items()}
        
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(settings, file)

    def setup_gui(self):
        self.setup_menu()
        self.setup_header()
        self.setup_status_bar()
        
        for app_name, app_data in self.apps.items():
            self.create_app_frame(app_name, app_data)

    def setup_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.window.quit)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def setup_header(self):
        style = ttk.Style()
        style.configure('TButton', padding=6, relief="flat", background="#ccc")
        
        header = tk.Frame(self.window, bg='#f0f0f0')
        header.pack(fill=tk.X, padx=20, pady=20)
        
        title = tk.Label(header, 
                        text="Social Media Timer & Blocker",
                        font=("Helvetica", 24, "bold"),
                        bg='#f0f0f0')
        title.pack()

    def setup_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to Social Media Timer & Blocker")
        
        status_bar = tk.Label(self.window, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_about(self):
        messagebox.showinfo("About", "Social Media Timer & Blocker\nVersion 1.0")

    def create_app_frame(self, app_name, app_data):
        frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, bg='white')
        frame.pack(pady=10, padx=20, fill=tk.X)
        
        app_label = tk.Label(frame, 
                            text=app_name,
                            font=("Helvetica", 14, "bold"),
                            fg=app_data["color"],
                            bg='white')
        app_label.pack(side=tk.LEFT, padx=10)
        
        time_frame = tk.Frame(frame, bg='white')
        time_frame.pack(side=tk.LEFT, padx=10)
        
        # Replace Entry widgets with Spinboxes
        hours_var = tk.StringVar(value="1")
        hours_spin = ttk.Spinbox(time_frame, 
                                from_=0, 
                                to=23, 
                                width=3, 
                                textvariable=hours_var,
                                wrap=True,
                                justify=tk.CENTER)
        hours_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="h", bg='white').pack(side=tk.LEFT)
        
        minutes_var = tk.StringVar(value="0")
        minutes_spin = ttk.Spinbox(time_frame, 
                                from_=0, 
                                to=59, 
                                width=3, 
                                textvariable=minutes_var,
                                wrap=True,
                                justify=tk.CENTER)
        minutes_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="m", bg='white').pack(side=tk.LEFT)
        
        seconds_var = tk.StringVar(value="0")
        seconds_spin = ttk.Spinbox(time_frame, 
                                from_=0, 
                                to=59, 
                                width=3, 
                                textvariable=seconds_var,
                                wrap=True,
                                justify=tk.CENTER)
        seconds_spin.pack(side=tk.LEFT)
        tk.Label(time_frame, text="s", bg='white').pack(side=tk.LEFT)
        
        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(side=tk.LEFT, padx=10)
        
        start_btn = ttk.Button(btn_frame,
                              text="Start",
                              command=lambda: self.start_timer(app_name))
        start_btn.pack(side=tk.LEFT, padx=5)
        
        block_btn = ttk.Button(btn_frame,
                              text="Block",
                              command=lambda: self.toggle_block(app_name))
        block_btn.pack(side=tk.LEFT, padx=5)
        
        timer_label = tk.Label(frame,
                              text="00:00:00",
                              font=("Helvetica", 14),
                              bg='white')
        timer_label.pack(side=tk.LEFT, padx=10)
        
        cooldown_label = tk.Label(frame,
                                text="",
                                font=("Helvetica", 10),
                                fg="red",
                                bg='white')
        cooldown_label.pack(side=tk.LEFT, padx=10)
        
        self.apps[app_name].update({
            "hours_var": hours_var,
            "minutes_var": minutes_var,
            "seconds_var": seconds_var,
            "timer_label": timer_label,
            "cooldown_label": cooldown_label,
            "block_btn": block_btn,
            "start_btn": start_btn
        })

    def start_timer(self, app_name):
        if time.time() < self.apps[app_name]["cooldown_until"]:
            remaining = int(self.apps[app_name]["cooldown_until"] - time.time())
            messagebox.showwarning("Cooldown Active", 
                f"Please wait {remaining//60}m {remaining%60}s before using {app_name}")
            return
        
        hours = int(self.apps[app_name]["hours_var"].get())
        minutes = int(self.apps[app_name]["minutes_var"].get())
        seconds = int(self.apps[app_name]["seconds_var"].get())
        
        total_seconds = hours * 3600 + minutes * 60 + seconds
        self.apps[app_name]["time_remaining"] = total_seconds
        self.apps[app_name]["is_running"] = True
        self.apps[app_name]["start_btn"].config(state="disabled")
        
        if self.apps[app_name]["is_blocked"]:
            self.toggle_block(app_name)
        
        self.save_settings()

    def toggle_block(self, app_name):
        if self.apps[app_name]["is_blocked"]:
            self.unblock_site(app_name)
            self.show_notification(f"{app_name} Unblocked", f"{app_name} has been unblocked.")
        else:
            self.block_site(app_name)
            self.show_notification(f"{app_name} Blocked", f"{app_name} has been blocked.")
        
        self.save_settings()

    def block_site(self, app_name):
        try:
            with open(self.hosts_path, 'a') as hosts_file:
                for url in self.apps[app_name]["urls"]:
                    hosts_file.write(f"\n{self.redirect} {url}")
            os.system('ipconfig /flushdns')
            self.apps[app_name]["is_blocked"] = True
            self.apps[app_name]["block_btn"].config(text="Unblock")
        except PermissionError:
            messagebox.showerror("Error", "Please run as administrator!")

    def unblock_site(self, app_name):
        try:
            with open(self.hosts_path, 'r') as hosts_file:
                lines = hosts_file.readlines()
            with open(self.hosts_path, 'w') as hosts_file:
                for line in lines:
                    if not any(url in line for url in self.apps[app_name]["urls"]):
                        hosts_file.write(line)
            os.system('ipconfig /flushdns')
            self.apps[app_name]["is_blocked"] = False
            self.apps[app_name]["block_btn"].config(text="Block")
        except PermissionError:
            messagebox.showerror("Error", "Please run as administrator!")

    def force_close_tabs(self, app_name):
        close_script = f"""
        $browsers = @('chrome', 'firefox', 'msedge')
        $domain = '{self.apps[app_name]["domain"]}'
        foreach ($browser in $browsers) {{
            try {{
                $proc = Get-Process $browser -ErrorAction SilentlyContinue
                if ($proc) {{
                    $proc | ForEach-Object {{
                        $handle = $_.MainWindowHandle
                        if ($handle -and $_.MainWindowTitle -like "*$domain*") {{
                            Add-Type -AssemblyName System.Windows.Forms
                            [System.Windows.Forms.SendKeys]::SendWait('^w')
                            Start-Sleep -Milliseconds 100
                        }}
                    }}
                }}
            }} catch {{ }}
        }}
        """
        subprocess.run(['powershell', '-Command', close_script], capture_output=True, text=True)

    def get_active_window_title(self):
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            return win32gui.GetWindowText(window).lower()
        except:
            return ""

    def monitor_windows(self):
        while True:
            active_window = self.get_active_window_title()
            current_time = time.time()
            
            for app_name, app_data in self.apps.items():
                if current_time < app_data["cooldown_until"]:
                    remaining = int(app_data["cooldown_until"] - current_time)
                    app_data["cooldown_label"].config(
                        text=f"Cooldown: {remaining//60}m {remaining%60}s")
                    
                    if app_data["domain"] in active_window:
                        self.force_close_tabs(app_name)
                else:
                    app_data["cooldown_label"].config(text="")
                    
                if app_data["is_running"]:
                    if app_data["domain"] in active_window:
                        app_data["time_remaining"] -= 1
                        if app_data["time_remaining"] <= 0:
                            self.window.after(0, lambda n=app_name: self.time_up(n))
                    self.update_timer_display(app_name)
            time.sleep(1)

    def time_up(self, app_name):
        self.force_close_tabs(app_name)
        self.block_site(app_name)
        
        self.apps[app_name]["is_running"] = False
        self.apps[app_name]["cooldown_until"] = time.time() + self.cooldown_period
        self.apps[app_name]["start_btn"].config(state="disabled")
        
        messagebox.showwarning("Time's Up!", 
            f"Time's up for {app_name}!\nSite will be blocked for 15 minutes.")
        
        self.show_notification(f"Time's Up for {app_name}", f"{app_name} has been blocked for 15 minutes.")
        
        self.window.after(self.cooldown_period * 1000, 
                         lambda: self.end_cooldown(app_name))

    def end_cooldown(self, app_name):
        self.apps[app_name]["start_btn"].config(state="normal")
        self.apps[app_name]["cooldown_label"].config(text="")
        messagebox.showinfo("Cooldown Ended", 
            f"You can now use {app_name} again.")
        
        self.show_notification(f"Cooldown Ended for {app_name}", f"You can now use {app_name} again.")

    def update_timer_display(self, app_name):
        remaining = self.apps[app_name]["time_remaining"]
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60
        seconds = remaining % 60
        
        self.apps[app_name]["timer_label"].config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self.monitor_windows, daemon=True)
        monitor_thread.start()

    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            timeout=10
        )

    def run(self):
        self.window.mainloop()
