import serial
import time
from datetime import datetime
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import winsound  # Windows only; comment out on Mac/Linux

# ---------- CONFIG ----------
SERIAL_PORT = 'COM20'
BAUD_RATE = 9600

ALERT_THRESHOLD = 650
SUSTAINED_READINGS = 5
MAX_POINTS = 100
LOG_FILE = "gas_log.csv"

# ---------- STATE ----------
readings = deque(maxlen=MAX_POINTS)
timestamps = deque(maxlen=MAX_POINTS)
recent_check = deque(maxlen=SUSTAINED_READINGS)
alert_active = False
start_time = time.time()

# ---------- SERIAL SETUP ----------
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT}. Starting dashboard...\n")
except serial.SerialException as e:
    print(f"Could not open {SERIAL_PORT}: {e}")
    exit()

# ---------- PLOT SETUP ----------
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot([], [], color='green', linewidth=2)
ax.axhline(y=ALERT_THRESHOLD, color='red', linestyle='--', label='Alert Threshold')
ax.set_ylim(0, 1023)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Raw Sensor Value")
ax.set_title("MQ-4 Gas Sensor — Live Dashboard")
ax.legend(loc='upper right')
status_text = ax.text(0.02, 0.95, "Status: Monitoring", transform=ax.transAxes,
                       fontsize=12, verticalalignment='top',
                       bbox=dict(boxstyle="round", facecolor="lightgreen"))

def log_event(raw_value):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()},{raw_value}\n")

def trigger_alert(raw_value):
    print(f"\n🚨 GAS LEAK DETECTED at {datetime.now().strftime('%H:%M:%S')} | raw={raw_value} 🚨")
    log_event(raw_value)
    try:
        winsound.Beep(1500, 500)
    except:
        print("\a")

def update(frame):
    global alert_active

    line_data = ser.readline().decode('utf-8').strip()
    if not line_data or not line_data.isdigit():
        return line, status_text

    raw_value = int(line_data)
    elapsed = time.time() - start_time

    readings.append(raw_value)
    timestamps.append(elapsed)
    recent_check.append(raw_value)

    line.set_data(list(timestamps), list(readings))
    ax.set_xlim(max(0, elapsed - 30), elapsed + 1)

    is_leak = len(recent_check) == SUSTAINED_READINGS and all(v > ALERT_THRESHOLD for v in recent_check)

    if is_leak:
        if not alert_active:
            trigger_alert(raw_value)
            alert_active = True
        status_text.set_text(f"Status: 🚨 GAS LEAK ({raw_value})")
        status_text.set_bbox(dict(boxstyle="round", facecolor="red"))
        line.set_color('red')
    else:
        alert_active = False
        status_text.set_text(f"Status: Safe ({raw_value})")
        status_text.set_bbox(dict(boxstyle="round", facecolor="lightgreen"))
        line.set_color('green')

    return line, status_text

ani = animation.FuncAnimation(fig, update, interval=200, cache_frame_data=False)
plt.tight_layout()
plt.show()