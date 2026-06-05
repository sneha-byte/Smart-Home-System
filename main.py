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
from libs.utils import format_time

# initialize wifi and try to set time
init_wifi(secrets["ssid"], secrets["password"])

try:
    ntptime.settime()
except:
    pass

# set up i2c and lcd
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=10000)
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

# current button and current ldr value
last_button = button.value()
baseline_light = ldr.read_u16()

# main loop to check mode and take action
while True:
    current_button = button.value()
    # change mode to security if button has changed
    if current_button == 0 and last_button == 1:
        if mode == "NORMAL":
            mode = "SECURITY"
            baseline_light = ldr.read_u16()
            lcd.clear()
            lcd.write(0,0,"SECURITY MODE")
        else:
            mode = "NORMAL"
            lcd.clear()
            lcd.write(0,0,"NORMAL MODE")
        utime.sleep(1)

    last_button = current_button

    # normal mode
    if mode == "NORMAL":
        celsius, fahrenheit = read_temp(thermistor)
        led.value(1)
        lcd.clear()
        # lcd display temperature alternate between C and F every 2 seconds
        lcd.write(0, 0, "T:{:.1f}C".format(celsius))
        lcd.write(0, 1, "NORMAL MODE")
        utime.sleep(2)
        lcd.clear()
        lcd.write(0, 0, "T:{:.1f}F".format(fahrenheit))
        #lcd display time
        lcd.write(0,1,format_time()[11:])
        utime.sleep(2)
        print("Temp:",round(celsius, 1),"C")
        print("time:", utime.localtime()[3],utime.localtime()[4])

    # security mode
    else:
        #measure ldr and ultrasonic sensor
        light = ldr.read_u16()
        print("light:",light)
        distance = measure_distance(TRIG, ECHO)
        print("distance:",distance)
        lcd.clear()
        lcd.write(0,0,"SECURITY")
        lcd.write( 0,1, "Distance: {:.0f}cm".format(distance))
        time.sleep(4)
        lcd.clear()
        lcd.write(0,0,"SECURITY MODE")
        lcd.write(0,1,"LDR:{:5d}".format(light))
        time.sleep(2)
        suspicious = False
        event = ""

        # if distance is less than 20cm it is an alert
        if distance < DISTANCE_THRESHOLD:
            suspicious = True
            event = "Motion"
            print("ALERT: Motion",distance)

        # if the light change is greater than the light threshold it is an alert
        if abs(light - baseline_light) > LIGHT_THRESHOLD:
            suspicious = True
            event = "Light Change"
            print("ALERT: Light Change",light)

        # led is blinked when suspicious flag is true else it is off
        if suspicious:
            led.toggle()
            print("Time:",utime.localtime())
            current_time = utime.time()
            # send email if a good chunk of time has passed since last email and pass in event info
            if (current_time - last_email_time) > EMAIL_COOLDOWN:
                send_security_email(event, distance,light)
                last_email_time = current_time
        else:
            led.value(0)

    utime.sleep(0.5)