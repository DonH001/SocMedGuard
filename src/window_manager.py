import win32gui
import win32process

class WindowManager:
    @staticmethod
    def get_active_window_title():
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            return win32gui.GetWindowText(window).lower()
        except:
            return ""
