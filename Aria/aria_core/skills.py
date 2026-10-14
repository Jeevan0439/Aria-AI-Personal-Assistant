import os, subprocess, webbrowser, datetime, ctypes, time
import pyautogui, psutil
from PIL import ImageGrab

pyautogui.FAILSAFE = False

APPS = {
    "chrome":        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad":       "notepad.exe",
    "calculator":    "calc.exe",
    "file explorer": "explorer.exe",
    "vs code":       "code",
    "spotify":       "spotify.exe",
    "whatsapp":      "whatsapp:",
    "youtube":       "https://youtube.com",
    "instagram":     "https://instagram.com",
}

# ── Window focus ──────────────────────────────────────────
def focus_window(keyword):
    import ctypes
    EnumWindows     = ctypes.windll.user32.EnumWindows
    WNDENUMPROC     = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText   = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLen= ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    SetForeground   = ctypes.windll.user32.SetForegroundWindow
    ShowWindow      = ctypes.windll.user32.ShowWindow

    found = [None]
    def cb(hwnd, _):
        if IsWindowVisible(hwnd):
            l   = GetWindowTextLen(hwnd)
            buf = ctypes.create_unicode_buffer(l + 1)
            GetWindowText(hwnd, buf, l + 1)
            if keyword.lower() in buf.value.lower():
                found[0] = hwnd
                return False
        return True
    EnumWindows(WNDENUMPROC(cb), 0)
    if found[0]:
        ShowWindow(found[0], 9)
        SetForeground(found[0])
        time.sleep(0.4)
        return True
    return False

# ── Volume ────────────────────────────────────────────────
def volume_up(n=5):
    for _ in range(n):
        ctypes.windll.user32.keybd_event(0xAF, 0, 0x1, 0)
        ctypes.windll.user32.keybd_event(0xAF, 0, 0x3, 0)
    return "Volume up."

def volume_down(n=5):
    for _ in range(n):
        ctypes.windll.user32.keybd_event(0xAE, 0, 0x1, 0)
        ctypes.windll.user32.keybd_event(0xAE, 0, 0x3, 0)
    return "Volume down."

def mute():
    ctypes.windll.user32.keybd_event(0xAD, 0, 0x1, 0)
    ctypes.windll.user32.keybd_event(0xAD, 0, 0x3, 0)
    return "Toggled mute."

# ── Screenshot ────────────────────────────────────────────
def screenshot():
    path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop",
                        f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png")
    ImageGrab.grab().save(path)
    return "Screenshot saved to Desktop."

# ── Apps ──────────────────────────────────────────────────
def open_app(cmd):
    for name, path in APPS.items():
        if name in cmd:
            try:
                if path.startswith("http"):
                    webbrowser.open(path)
                elif path.endswith(":"):
                    os.system(f"start {path}")
                else:
                    subprocess.Popen(path)
                return f"Opening {name}."
            except Exception as e:
                return f"Couldn't open {name}: {e}"
    return None

def close_app(cmd):
    mapping = {
        "chrome": "chrome.exe", "spotify": "spotify.exe",
        "notepad": "notepad.exe", "vs code": "code.exe",
        "calculator": "calc.exe"
    }
    for name, exe in mapping.items():
        if name in cmd:
            os.system(f"taskkill /f /im {exe} >nul 2>&1")
            return f"Closed {name}."
    return None

# ── Spotify ───────────────────────────────────────────────
def spotify_play_pause():
    focus_window("Spotify")
    pyautogui.press("space")
    return "Toggled playback."

def spotify_next():
    focus_window("Spotify")
    pyautogui.hotkey("ctrl", "right")
    return "Next track."

def spotify_prev():
    focus_window("Spotify")
    pyautogui.hotkey("ctrl", "left")
    return "Previous track."

def spotify_search_play(song):
    if not focus_window("Spotify"):
        subprocess.Popen("spotify.exe")
        time.sleep(4)
        focus_window("Spotify")
    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "k")
    time.sleep(0.8)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(song, interval=0.06)
    time.sleep(2.0)
    # Click Songs tab to filter
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.press("tab")
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(1.0)
    # Play first result
    pyautogui.press("tab")
    time.sleep(0.2)
    pyautogui.press("enter")
    return f"Playing {song} on Spotify."

# ── WhatsApp ──────────────────────────────────────────────
def send_whatsapp(contact, message):
    if not focus_window("WhatsApp"):
        os.system("start whatsapp:")
        time.sleep(5)
        focus_window("WhatsApp")
    time.sleep(0.6)
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.8)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.typewrite(contact, interval=0.05)
    time.sleep(1.8)
    pyautogui.press("enter")
    time.sleep(1.0)
    pyautogui.typewrite(message, interval=0.04)
    time.sleep(0.3)
    pyautogui.press("enter")
    return f"Message sent to {contact}."

# ── PC Power ──────────────────────────────────────────────
def pc_power(cmd):
    if "shut down" in cmd or "shutdown" in cmd:
        os.system("shutdown /s /t 5"); return "Shutting down in 5 seconds."
    if "restart" in cmd:
        os.system("shutdown /r /t 5"); return "Restarting in 5 seconds."
    if "sleep" in cmd:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Sleeping now."
    return None

# ── Web search ────────────────────────────────────────────
def google_search(query):
    q = query.replace("search for","").replace("google","").replace("search","").strip()
    webbrowser.open(f"https://www.google.com/search?q={q.replace(' ','+')}")
    return f"Searching Google for {q}."

# ── Reminders ─────────────────────────────────────────────
import threading, re
from plyer import notification

def parse_reminder(cmd):
    m = re.search(r"remind(?:er)? (?:me )?(?:at|in) (.+?) (?:to|that) (.+)", cmd)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None, None

def parse_time_seconds(time_str):
    now = datetime.datetime.now()
    time_str = time_str.lower().strip()
    m = re.search(r"(\d+) minute", time_str)
    if m: return int(m.group(1)) * 60
    m = re.search(r"(\d+) hour", time_str)
    if m: return int(m.group(1)) * 3600
    m = re.search(r"(\d+) second", time_str)
    if m: return int(m.group(1))
    formats = ["%I%p","%I:%M%p","%I %p","%I:%M %p","%H:%M"]
    ts = time_str.replace(" ","").upper()
    for fmt in formats:
        try:
            t = datetime.datetime.strptime(ts, fmt)
            target = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
            if target <= now: target += datetime.timedelta(days=1)
            return int((target - now).total_seconds())
        except: continue
    return None

_speak_fn = None  # set by main.py

def set_reminder(time_str, message):
    secs = parse_time_seconds(time_str)
    if secs is None: return f"Couldn't understand the time '{time_str}'."
    def _fire():
        time.sleep(secs)
        if _speak_fn: _speak_fn(f"Jeevan, reminder — {message}")
        try:
            notification.notify(title="Aria Reminder", message=message, timeout=10)
        except: pass
    threading.Thread(target=_fire, daemon=True).start()
    mins = secs // 60
    if mins < 1: return f"Reminder set for {secs} seconds — {message}"
    if mins < 60: return f"Reminder set for {mins} minutes — {message}"
    return f"Reminder set for {time_str} — {message}"