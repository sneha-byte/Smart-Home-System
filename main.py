import time

from libs.lcd1602 import LCD
from machine import Pin, I2C, ADC
import utime
import ntptime
from libs.thermistor import read_temp
from libs.ultrasonic import measure_distance
from libs.wifi import init_wifi
from libs.email_alert import send_security_email
from libs.secrets import secrets

init_wifi(secrets["ssid"], secrets["password"])

try:
    ntptime.settime()
except:
    pass

i2c = I2C(
    0,
    sda=Pin(0),
    scl=Pin(1),
    freq=10000
)

lcd = LCD(i2c)

# thermistor and ldr and ultrasonic
thermistor = ADC(27)
ldr = ADC(26)

TRIG = Pin(19, Pin.OUT)
ECHO = Pin(18, Pin.IN)

# button and led
button = Pin(15, Pin.IN)

led = Pin(16, Pin.OUT)

# config
LIGHT_THRESHOLD = 10000
DISTANCE_THRESHOLD = 20
EMAIL_COOLDOWN = 200
last_email_time = 0

#start with normal mode
mode = "NORMAL"

last_button = button.value()
baseline_light = ldr.read_u16()

# -----------------------
# MAIN LOOP
# -----------------------

while True:

    current_button = button.value()

    if current_button == 0 and last_button == 1:

        if mode == "NORMAL":

            mode = "SECURITY"

            baseline_light = ldr.read_u16()

            lcd.clear()
            lcd.write(
                0,
                0,
                "SECURITY MODE"
            )

            lcd.write(
                0,
                1,
                "ARMED"
            )

        else:

            mode = "NORMAL"

            lcd.clear()

            lcd.write(
                0,
                0,
                "NORMAL MODE"
            )

        utime.sleep(1)

    last_button = current_button

    # -----------------------
    # NORMAL MODE
    # -----------------------

    if mode == "NORMAL":

        celsius, fahrenheit = read_temp(
            thermistor
        )

        led.value(1)

        lcd.clear()
        lcd.write(0, 0, "T:{:.1f}C".format(celsius))
        lcd.write(0, 1, "NORMAL MODE")
        utime.sleep(2)

        lcd.clear()
        lcd.write(0, 0, "T:{:.1f}F".format(fahrenheit))
        lcd.write(
            0,
            1,
            "{:02d}:{:02d}".format(
                utime.localtime()[3],
                utime.localtime()[4]
            )
        )
        utime.sleep(2)



        print(
            "Temp:",
            round(celsius, 1),
            "C"
        )

    # -----------------------
    # SECURITY MODE
    # -----------------------

    else:

        light = ldr.read_u16()

        distance = measure_distance(
            TRIG,
            ECHO
        )

        lcd.clear()

        lcd.write(
            0,
            0,
            "SECURITY"
        )

        lcd.write(
            0,
            1,
            "{:.0f}cm".format(
                distance
            )
        )

        suspicious = False
        event = ""

        if distance < DISTANCE_THRESHOLD:

            suspicious = True
            event = "Motion"

            print(
                "ALERT: Motion",
                distance
            )

        if abs(
                light -
                baseline_light
        ) > LIGHT_THRESHOLD:

            suspicious = True
            event = "Light Change"

            print(
                "ALERT: Light Change",
                light
            )

        if suspicious:

            led.toggle()

            print(
                "Time:",
                utime.localtime()
            )

            current_time = utime.time()

            if (
                current_time -
                last_email_time
            ) > EMAIL_COOLDOWN:

                send_security_email(
                    event,
                    distance,
                    light
                )

                last_email_time = current_time

        else:

            led.value(0)

    utime.sleep(0.5)