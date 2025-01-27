import os
import subprocess
from tkinter import messagebox

class SiteBlocker:
    def __init__(self, hosts_path, redirect_ip):
        self.hosts_path = hosts_path
        self.redirect_ip = redirect_ip

    def block_site(self, urls):
        try:
            with open(self.hosts_path, 'a') as hosts_file:
                for url in urls:
                    hosts_file.write(f"\n{self.redirect_ip} {url}")
            self._flush_dns()
            return True
        except PermissionError:
            messagebox.showerror("Error", "Please run the program as administrator!")
            return False

    def unblock_site(self, urls):
        try:
            with open(self.hosts_path, 'r') as hosts_file:
                lines = hosts_file.readlines()
            
            with open(self.hosts_path, 'w') as hosts_file:
                for line in lines:
                    if not any(url in line for url in urls):
                        hosts_file.write(line)
            self._flush_dns()
            return True
        except PermissionError:
            messagebox.showerror("Error", "Please run the program as administrator!")
            return False

    def _flush_dns(self):
        os.system('ipconfig /flushdns')

    @staticmethod
    def force_close_tabs(domain):
        close_script = f"""
        $browsers = @('chrome', 'firefox', 'msedge')
        $domain = '{domain}'
        
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
