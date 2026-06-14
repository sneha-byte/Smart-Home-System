# Smart Home Security System Using Raspberry Pi Pico W

A smart home security system built with the Raspberry Pi Pico W and MicroPython. The system operates in two modes: **Normal Mode** and **Security Mode**. In Normal Mode, it monitors ambient temperature and displays the current time. In Security Mode, it monitors motion and light level changes to detect potential intrusions and sends email notifications when suspicious activity is detected.

## Features

- Real-time temperature monitoring using a thermistor
- Displays temperature in both Celsius and Fahrenheit
- Internet-synchronized clock using NTP
- Motion detection using an HC-SR04 ultrasonic sensor
- Light change detection using an LDR (photoresistor)
- Mode switching using a push button
- LCD status display
- LED status indicators and alerts
- Wi-Fi connectivity using Raspberry Pi Pico W
- Email notifications through Gmail SMTP

---

## Hardware Components

| Component | Quantity |
|------------|-----------|
| Raspberry Pi Pico W | 1 |
| HC-SR04 Ultrasonic Sensor | 1 |
| Thermistor | 1 |
| Photoresistor (LDR) | 1 |
| 16x2 I2C LCD Display | 1 |
| Push Button | 1 |
| LED | 1 |
| 220 Ω Resistor | 1 |
| 10 kΩ Resistor (Button Pull-up) | 1 |
| 10 kΩ Resistor (Thermistor Voltage Divider) | 1 |
| 10 kΩ Resistor (LDR Voltage Divider) | 1 |
| Breadboard | 1 |
| Jumper Wires | Multiple |

---

## Circuit Diagram

<img width="484" height="445" alt="image" src="https://github.com/user-attachments/assets/ad9e3ec7-95f2-400a-b81b-2d7941dbe59a" />


---

## Wiring

### LCD Display (I2C)

| LCD Pin | Pico W Pin |
|----------|------------|
| SDA | GP0 |
| SCL | GP1 |
| VCC | VBUS |
| GND | GND |

The LCD communicates with the Pico W using the I2C protocol, reducing the number of GPIO pins required.

### Thermistor

| Connection | Pico W Pin |
|------------|------------|
| Output | GP27 (ADC1) |

The thermistor is connected in a voltage divider configuration with a 10 kΩ resistor. The analog voltage is converted into temperature using the Beta parameter equation.

### LDR

| Connection | Pico W Pin |
|------------|------------|
| Output | GP26 (ADC0) |

The LDR is connected as a voltage divider and continuously monitors ambient light levels.

### Ultrasonic Sensor (HC-SR04)

| Sensor Pin | Pico W Pin |
|------------|------------|
| Trigger | GP19 |
| Echo | GP18 |
| VCC | 3.3V |
| GND | GND |

### Push Button

| Component | Pico W Pin |
|------------|------------|
| Button | GP15 |

Configured with a 10 kΩ pull-up resistor.

### LED

| Component | Pico W Pin |
|------------|------------|
| LED | GP16 |

Connected through a 220 Ω current-limiting resistor.

---

## Project Photos

### Completed Circuit

<img width="293" height="221" alt="image" src="https://github.com/user-attachments/assets/08ae8ec0-c33a-4583-abbb-2b738435a463" />
<img width="294" height="219" alt="image" src="https://github.com/user-attachments/assets/83e7f51c-164a-4b7c-8890-627e1a3c653a" />


### Security Mode

<img width="319" height="241" alt="image" src="https://github.com/user-attachments/assets/bfd59e2c-0fbe-4c7d-b8c6-00173749abce" />


### Normal Mode

<img width="320" height="241" alt="image" src="https://github.com/user-attachments/assets/981d6c94-77ad-41b9-bccf-3c5ba0e518a8" />

---

# System Operation

## Normal Mode

When powered on, the system starts in Normal Mode.

### Functions

- Reads ambient temperature from the thermistor
- Converts temperature to Celsius and Fahrenheit
- Synchronizes time using an NTP server
- Displays temperature, time, and current mode on the LCD
- LED remains ON to indicate normal operation

### LCD Display Example

```text
T:24.2 C
NORMAL MODE
```

```text
T:75.6 F
12:49 PM
```

---

## Security Mode

Pressing the push button switches the system into Security Mode.

### Functions

- Stores the current LDR reading as a baseline
- Continuously measures distance using the ultrasonic sensor
- Continuously monitors ambient light levels
- Alternates LCD display between distance and light readings

### LCD Display Example

```text
SECURITY
Distance: 15 cm
```

```text
SECURITY MODE
LDR: 24453
```

---

## Intrusion Detection

The system uses two detection methods:

### Motion Detection

An alert is triggered when an object is detected within:

```text
20 cm
```

of the ultrasonic sensor.

### Light Change Detection

An alert is triggered when the LDR value changes by more than:

```text
10,000 ADC counts
```

from the stored baseline value.

### Alert Actions

When suspicious activity is detected:

- LED begins blinking
- Event information is printed to the serial console
- Email notification is sent
- 200-second cooldown prevents repeated email spam

---

# Email Notification System

The Raspberry Pi Pico W connects to Wi-Fi and uses Gmail SMTP services to send security alerts.

The email includes:

- Security mode status
- Event type
- Ultrasonic distance measurement
- Light sensor reading
- Timestamp

### Example Alert

<img width="544" height="257" alt="image" src="https://github.com/user-attachments/assets/8d7b9aa4-3851-45c6-a8c1-c712df945d3b" />

---

# Software Structure

## Libraries Used

| Library | Purpose |
|----------|----------|
| network | Wi-Fi networking |
| network.WLAN | Wireless LAN management |
| time | Timing functions |
| utime | Timestamps and delays |
| ntptime | NTP synchronization |
| machine | GPIO, ADC, and I2C access |
| umail | Gmail SMTP email support |
| lcd1602 | LCD display control |

---

## File Structure

```text
Smart-Home-Security-System/
│
├── main.py
├── thermistor.py
├── ultrasonic.py
├── wifi.py
├── email_alert.py
├── utils.py
├── secrets.py
├── images/
└── README.md
```

### main.py

Handles:

- Mode switching
- Sensor monitoring
- LCD updates
- Alert generation
- Email notification triggering

### thermistor.py

Converts ADC readings into Celsius and Fahrenheit temperatures using the thermistor Beta equation.

### ultrasonic.py

Measures distance using the HC-SR04 ultrasonic sensor by timing the return echo pulse.

### wifi.py

Handles Wi-Fi initialization and connection management for the Pico W.

### email_alert.py

Creates a secure SMTP connection to Gmail and sends security alert emails.

### utils.py

Formats NTP-synchronized timestamps for LCD display and email messages.


# Future Improvements

- Add PIR motion sensor support
- Mobile application integration
- Cloud logging and analytics
- Camera-based image capture on intrusion
- SMS notifications
- Multiple user notifications
- Battery backup support

---

# Technologies Used

- Raspberry Pi Pico W
- MicroPython
- HC-SR04 Ultrasonic Sensor
- I2C LCD Display
- Gmail SMTP
- NTP Time Synchronization
- Breadboard Prototyping


