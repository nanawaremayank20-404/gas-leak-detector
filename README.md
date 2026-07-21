# 🔥 Gas Leak Detection System using Arduino Uno, MQ-4 Sensor & Python Dashboard

## 📌 Overview

This project is a real-time gas leak detection system built using an Arduino Uno and MQ-4 gas sensor. The Arduino continuously monitors methane gas levels and sends the data to a Python dashboard through serial communication.

The dashboard displays live gas readings and alerts the user when the gas concentration exceeds a predefined threshold.

---

## Features

- Real-time gas monitoring
- Live Python dashboard
- Arduino-Python serial communication
- MQ-4 methane gas sensor
- Gas leak warning
- Easy to modify and expand

---

## Hardware Used

- Arduino Uno
- MQ-4 Gas Sensor
- USB Cable
- Breadboard
- Jumper Wires
- Laptop/PC

---

## Software Used

- Arduino IDE
- Python 3
- VS Code

Python Libraries:

- pyserial
- tkinter (or your dashboard library)
- matplotlib (if used)
- pandas (if used)

Install libraries:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
Arduino/
Python/

README.md
```

---

## Working

1. MQ-4 detects methane gas.
2. Arduino reads the analog value.
3. Arduino sends the value through Serial.
4. Python receives the data.
5. Dashboard displays live readings.
6. Alert is shown if gas level exceeds the threshold.

---

## Circuit Connections

| MQ-4 | Arduino |
|------|----------|
| VCC | 5V |
| GND | GND |
| AO | A0 |

---

## How to Run

### Upload Arduino Code

1. Open Arduino IDE
2. Open `Gas_Detection.ino`
3. Select Arduino Uno
4. Upload the code

### Run Python Dashboard

```bash
cd Python

python dashboard.py
```

---

## Future Improvements

- Email Alerts
- SMS Notifications
- IoT Cloud Monitoring
- Mobile App
- ESP32 WiFi Support

---

## Author

Mayank Nanaware

First Year Electronics & Communication Engineering

MIT Vishwaprayag University, Solapur

GitHub: https://github.com/YOUR_USERNAME
