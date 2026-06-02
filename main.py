from libs.lcd1602 import LCD
from machine import Pin, I2C, ADC
import utime
from libs.ultrasonic import measure_distance
from libs.thermistor import read_temp

# LCD init
i2c = I2C(
    0,
    sda=Pin(0),
    scl=Pin(1),
    freq=10000
)
lcd = LCD(i2c)

# Thermistor
thermistor = ADC(27)

# button
button = Pin(15, Pin.IN)

# LED
led = Pin(16, Pin.OUT)


TRIG = Pin(19, Pin.OUT)
ECHO = Pin(18, Pin.IN)

while True:
    dist = measure_distance(TRIG, ECHO)
    print(f"{dist:.2f} cm")
    utime.sleep(0.5)





