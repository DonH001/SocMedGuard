import ctypes
from tkinter import messagebox

def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showwarning("Admin Rights Required",
            "Please run as administrator for blocking features!")
    
    from src.app import SocialMediaBlocker
    app = SocialMediaBlocker()
    app.run()

if __name__ == "__main__":
    main()
    