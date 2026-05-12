import tkinter as tk
import pygetwindow as gw
import psutil
import time
import threading
import requests
import sys
import traceback
import socket



# =========================
# AUTO DISCOVER SERVER
# =========================


def find_server():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 80))

    local_ip = s.getsockname()[0]

    s.close()

    print("LOCAL IP:", local_ip)

    parts = local_ip.split(".")

    base_ip = f"{parts[0]}.{parts[1]}.{parts[2]}."

    print("SCANNING:", base_ip)

    for i in range(1, 255):

        ip = base_ip + str(i)

        url = f"http://{ip}:5000/discover"

        try:

            r = requests.get(url, timeout=0.03)

            if r.status_code == 200:

                data = r.json()

                if data.get("name") == "study-guard":

                    print("SERVER FOUND:", ip)

                    return ip

        except:
            pass

    return None

# =========================
# INIT SERVER URL
# =========================

server_ip = find_server()

if not server_ip:
    print("SERVER NOT FOUND")
    input("ENTER TO EXIT...")
    sys.exit()

SERVER_URL = f"http://{server_ip}:5000/status"

print("SERVER URL:", SERVER_URL)

# =========================
# GLOBAL
# =========================

overlay = None
overlay_until = 0

# =========================
# DETECT YOUTUBE
# =========================

def youtube_detected():
    windows = gw.getAllTitles()

    for title in windows:
        if "YouTube" in title:
            return True

    return False

# =========================
# OVERLAY
# =========================

def close_overlay():
    global overlay

    if overlay is not None:
        try:
            overlay.destroy()
        except:
            pass

        overlay = None

def create_overlay(message):
    global overlay

    overlay = tk.Tk()
    overlay.attributes("-fullscreen", True)
    overlay.attributes("-topmost", True)
    overlay.configure(bg="#1e1e1e")

    tk.Label(
        overlay,
        text="⚠ MODE BELAJAR AKTIF",
        font=("Arial", 40, "bold"),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=50)

    tk.Label(
        overlay,
        text=message,
        font=("Arial", 20),
        fg="white",
        bg="#1e1e1e"
    ).pack(pady=20)

    tk.Button(
        overlay,
        text="Saya Akan Kembali Belajar 😭",
        font=("Arial", 18),
        command=close_overlay
    ).pack(pady=40)

    overlay.mainloop()

def show_overlay(message, duration=5):
    global overlay_until

    overlay_until = time.time() + duration

    if overlay is None:
        threading.Thread(
            target=create_overlay,
            args=(message,),
            daemon=True
        ).start()

# =========================
# SERVER STATUS CHECK
# =========================

def study_mode_active():
    try:
        r = requests.get(SERVER_URL, timeout=5)
        data = r.json()
        return data["blocked"]

    except:
        return False

# =========================
# ROBLOX BLOCKER
# =========================

blocked_apps = [
    "RobloxPlayerBeta.exe"
]

def roblox_detected():
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'] in blocked_apps:
                show_overlay("Roblox tidak diperbolehkan 😭", 5)
                time.sleep(1)
                process.kill()
                return True
        except:
            pass

    return False

# =========================
# MAIN LOOP
# =========================

def monitor():
    global overlay_until

    while True:
        try:
            if not study_mode_active():
                close_overlay()
                time.sleep(2)
                continue

            if youtube_detected():
                show_overlay("YouTube tidak diperbolehkan 😭", 999999)

            elif roblox_detected():
                pass

            else:
                if time.time() > overlay_until:
                    close_overlay()

        except Exception as e:
            print("ERROR:", e)

        time.sleep(1)

# =========================
# START
# =========================

try:
    monitor()

except Exception as e:
    print("FATAL ERROR")
    traceback.print_exc()
    input("ENTER TO EXIT...")