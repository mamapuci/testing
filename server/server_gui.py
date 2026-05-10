from flask import Flask, jsonify
import threading
import tkinter as tk

# =========================
# FLASK SERVER
# =========================

app = Flask(__name__)

study_mode = {
    "blocked": False
}

@app.route("/")
def home():
    return "Study Server Running"

@app.route("/status")
def status():
    return jsonify(study_mode)

@app.route("/start")
def start():
    study_mode["blocked"] = True
    return "Study mode ON"

@app.route("/stop")
def stop():
    study_mode["blocked"] = False
    return "Study mode OFF"

# ⭐ AUTO DISCOVERY ENDPOINT
@app.route("/discover")
def discover():
    return jsonify({
        "name": "study-guard",
        "port": 5000
    })

@app.route("/ping")
def ping():
    return "ok"

# =========================
# RUN SERVER
# =========================

def run_server():
    app.run(
        host="0.0.0.0",
        port=5000
    )

# =========================
# GUI
# =========================

def start_class():
    study_mode["blocked"] = True
    status_label.config(text="CLASS STATUS: ACTIVE 🔥")

def stop_class():
    study_mode["blocked"] = False
    status_label.config(text="CLASS STATUS: OFF")

window = tk.Tk()
window.title("Study Guard Server")
window.geometry("400x300")

title = tk.Label(
    window,
    text="STUDY GUARD",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

status_label = tk.Label(
    window,
    text="CLASS STATUS: OFF",
    font=("Arial", 16)
)
status_label.pack(pady=20)

start_button = tk.Button(
    window,
    text="START CLASS",
    font=("Arial", 16),
    width=20,
    height=2,
    bg="green",
    fg="white",
    command=start_class
)
start_button.pack(pady=10)

stop_button = tk.Button(
    window,
    text="STOP CLASS",
    font=("Arial", 16),
    width=20,
    height=2,
    bg="red",
    fg="white",
    command=stop_class
)
stop_button.pack(pady=10)

# =========================
# START SERVER THREAD
# =========================

server_thread = threading.Thread(
    target=run_server,
    daemon=True
)
server_thread.start()

# =========================
# START GUI
# =========================

window.mainloop()