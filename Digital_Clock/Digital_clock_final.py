import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
import pygame

pygame.mixer.init()


def set_alarm():
    h = hour_var.get()
    m = minute_var.get()
    s = second_var.get()
    am_pm = am_pm_var.get()
    global alarm_time
    alarm_time = f"{h}:{m}:{s} {am_pm}"
    alarm_status.config(text=f"⏰  Alarm set for  {alarm_time}")


def check_alarm():
    global alarm_time
    if alarm_time:
        now = datetime.now().strftime("%I:%M:%S %p")
        if alarm_time == now:
            trigger_alarm()


def trigger_alarm():
    alarm_status.config(text="🚨  ALARM RINGING!", fg="#ff4444")
    play_alarm_sound()


def play_alarm_sound():
    try:
        pygame.mixer.music.load("aggressive-rising-alarm-fx-wide_140bpm.wav")
        pygame.mixer.music.play(loops=-1)
    except Exception as e:
        print("Error playing sound:", e)


def stop_alarm_sound():
    try:
        pygame.mixer.music.stop()
        alarm_status.config(text="✅  Alarm stopped", fg="#aaffaa")
        global alarm_time
        alarm_time = None
    except:
        pass


cities = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Dubai": "Asia/Dubai",
    "Paris": "Europe/Paris",
    "Moscow": "Europe/Moscow",
    "Singapore": "Asia/Singapore",
    "Los Angeles": "America/Los_Angeles",
    "Toronto": "America/Toronto",
}


def update_time():
    now = datetime.now()
    local = now.strftime("%I:%M:%S %p")
    date_str = now.strftime("%A, %B %d  %Y")
    local_time_label.config(text=local)
    date_label.config(text=date_str)
    check_alarm()

    city1 = city1_var.get()
    city2 = city2_var.get()

    try:
        tz1 = pytz.timezone(cities[city1])
        tz2 = pytz.timezone(cities[city2])
        time1 = datetime.now(tz1).strftime("%I:%M:%S %p")
        time2 = datetime.now(tz2).strftime("%I:%M:%S %p")
        city1_label.config(text=time1)
        city2_label.config(text=time2)
    except Exception:
        city1_label.config(text="Error")
        city2_label.config(text="Error")

    root.after(1000, update_time)


# ── Root ──────────────────────────────────────────────────────────────────────
BG       = "#0d1117"
CARD     = "#161b22"
ACCENT   = "#58a6ff"
GREEN    = "#3fb950"
ORANGE   = "#e3b341"
RED      = "#f85149"
FG       = "#e6edf3"
MUTED    = "#8b949e"

root = tk.Tk()
root.title("Digital Clock")
root.geometry("640x660")
root.configure(bg=BG)
root.resizable(False, False)

alarm_time = None

# ttk style
style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox",
    fieldbackground=CARD, background=CARD,
    foreground=FG, arrowcolor=ACCENT,
    bordercolor="#30363d", relief="flat", padding=4)
style.map("TCombobox", fieldbackground=[("readonly", CARD)])

# ── Title bar area ─────────────────────────────────────────────────────────
tk.Label(root, text="DIGITAL CLOCK", font=("Segoe UI", 13, "bold"),
         bg=BG, fg=MUTED).pack(pady=(18, 0))

# ── Clock card ─────────────────────────────────────────────────────────────
clock_card = tk.Frame(root, bg=CARD, highlightbackground=ACCENT,
                      highlightthickness=2)
clock_card.pack(padx=40, pady=(8, 4), fill="x")

local_time_label = tk.Label(clock_card, text="",
    font=("Segoe UI Light", 54, "bold"), bg=CARD, fg=ACCENT)
local_time_label.pack(pady=(14, 0))

date_label = tk.Label(clock_card, text="",
    font=("Segoe UI", 12), bg=CARD, fg=MUTED)
date_label.pack(pady=(0, 14))

# ── Divider ────────────────────────────────────────────────────────────────
tk.Frame(root, bg="#30363d", height=1).pack(fill="x", padx=40, pady=6)

# ── Alarm card ─────────────────────────────────────────────────────────────
alarm_card = tk.Frame(root, bg=CARD, highlightbackground="#30363d",
                      highlightthickness=1)
alarm_card.pack(padx=40, pady=4, fill="x")

tk.Label(alarm_card, text="SET ALARM", font=("Segoe UI", 10, "bold"),
         bg=CARD, fg=MUTED).pack(pady=(10, 6))

picker_frame = tk.Frame(alarm_card, bg=CARD)
picker_frame.pack()

hour_var    = tk.StringVar(value="07")
minute_var  = tk.StringVar(value="00")
second_var  = tk.StringVar(value="00")
am_pm_var   = tk.StringVar(value="AM")

hours           = [f"{i:02}" for i in range(1, 13)]
minutes_seconds = [f"{i:02}" for i in range(60)]
ampm            = ["AM", "PM"]

cb_kw = dict(width=5, state="readonly", font=("Segoe UI", 12))

hour_cb   = ttk.Combobox(picker_frame, textvariable=hour_var,   values=hours,           **cb_kw)
minute_cb = ttk.Combobox(picker_frame, textvariable=minute_var, values=minutes_seconds, **cb_kw)
second_cb = ttk.Combobox(picker_frame, textvariable=second_var, values=minutes_seconds, **cb_kw)
ampm_cb   = ttk.Combobox(picker_frame, textvariable=am_pm_var,  values=ampm,            **cb_kw)

for i, (cb, lbl) in enumerate(zip(
        [hour_cb, minute_cb, second_cb, ampm_cb],
        ["HH", "MM", "SS", ""])):
    tk.Label(picker_frame, text=lbl, font=("Segoe UI", 8),
             bg=CARD, fg=MUTED).grid(row=0, column=i, padx=6)
    cb.grid(row=1, column=i, padx=6, pady=4)

hour_cb.current(6); minute_cb.current(0); second_cb.current(0); ampm_cb.current(0)

btn_frame = tk.Frame(alarm_card, bg=CARD)
btn_frame.pack(pady=(4, 10))

tk.Button(btn_frame, text="  Set Alarm  ",
    command=set_alarm,
    font=("Segoe UI", 11, "bold"), bg=ACCENT, fg="#0d1117",
    relief="flat", cursor="hand2", padx=10, pady=5
).grid(row=0, column=0, padx=8)

tk.Button(btn_frame, text="  Stop Alarm  ",
    command=stop_alarm_sound,
    font=("Segoe UI", 11, "bold"), bg=RED, fg="white",
    relief="flat", cursor="hand2", padx=10, pady=5
).grid(row=0, column=1, padx=8)

alarm_status = tk.Label(alarm_card, text="No alarm set",
    font=("Segoe UI", 11), bg=CARD, fg=ORANGE)
alarm_status.pack(pady=(0, 10))

# ── Divider ────────────────────────────────────────────────────────────────
tk.Frame(root, bg="#30363d", height=1).pack(fill="x", padx=40, pady=6)

# ── World clock card ───────────────────────────────────────────────────────
world_card = tk.Frame(root, bg=CARD, highlightbackground="#30363d",
                      highlightthickness=1)
world_card.pack(padx=40, pady=4, fill="x")

tk.Label(world_card, text="🌍  WORLD CLOCKS", font=("Segoe UI", 10, "bold"),
         bg=CARD, fg=MUTED).pack(pady=(10, 6))

cols = tk.Frame(world_card, bg=CARD)
cols.pack(padx=20, pady=(0, 14), fill="x")
cols.columnconfigure(0, weight=1)
cols.columnconfigure(1, weight=1)

city1_var = tk.StringVar(value="New York")
city2_var = tk.StringVar(value="London")

city_cb_kw = dict(values=list(cities.keys()), width=18, state="readonly",
                  font=("Segoe UI", 11))

city1_cb = ttk.Combobox(cols, textvariable=city1_var, **city_cb_kw)
city1_cb.grid(row=0, column=0, padx=10, pady=4)

city2_cb = ttk.Combobox(cols, textvariable=city2_var, **city_cb_kw)
city2_cb.grid(row=0, column=1, padx=10, pady=4)

city1_label = tk.Label(cols, text="", font=("Segoe UI Light", 22, "bold"),
                       bg=CARD, fg=GREEN)
city1_label.grid(row=1, column=0, padx=10)

city2_label = tk.Label(cols, text="", font=("Segoe UI Light", 22, "bold"),
                       bg=CARD, fg=GREEN)
city2_label.grid(row=1, column=1, padx=10)

# ── Start ──────────────────────────────────────────────────────────────────
update_time()
root.mainloop()
