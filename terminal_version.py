import serial
import time
from datetime import datetime
from collections import deque
import winsound  # Windows only; comment out on Mac/Linux and use print('\a') instead

# ---------- CONFIG ----------
SERIAL_PORT = 'COM20'       # change to your port
BAUD_RATE = 9600

ALERT_THRESHOLD = 650      # raw ADC value, tune after calibration
SUSTAINED_READINGS = 5
LOG_FILE = "gas_log.csv"

# ---------- STATE ----------
recent_readings = deque(maxlen=SUSTAINED_READINGS)
alert_active = False

def log_event(raw_value):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()},{raw_value}\n")

def trigger_alert(raw_value):
    print(f"\n🚨🚨 GAS LEAK DETECTED at {datetime.now().strftime('%H:%M:%S')} | raw={raw_value} 🚨🚨\n")
    log_event(raw_value)
    try:
        winsound.Beep(1500, 700)
    except:
        print("\a")

def main():
    global alert_active

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Connected to {SERIAL_PORT}. Monitoring for gas leaks...\n")
    except serial.SerialException as e:
        print(f"Could not open {SERIAL_PORT}: {e}")
        return

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line or not line.isdigit():
                continue

            raw_value = int(line)
            recent_readings.append(raw_value)
            print(f"\rRaw sensor value: {raw_value:4d}   ", end='')

            if len(recent_readings) == SUSTAINED_READINGS and all(v > ALERT_THRESHOLD for v in recent_readings):
                if not alert_active:
                    trigger_alert(raw_value)
                    alert_active = True
            else:
                alert_active = False

        except ValueError:
            continue
        except KeyboardInterrupt:
            print("\n\nStopped monitoring.")
            break

if __name__ == "__main__":
    main()