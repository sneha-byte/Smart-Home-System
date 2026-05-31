from lcd1602 import LCD
from machine import Pin, I2C, ADC
from time import sleep
import utime
import math

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

temperature_value = thermistor.read_u16()
Vr = 3.3 * float(temperature_value) / 65535
Rt = 10000 * Vr / (3.3 - Vr)
temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
Cel = temp - 273.15
Fah = Cel * 1.8 + 32
print('Celsius: %.2f C  Fahrenheit: %.2f F  Vr: %.2f' % (Cel, Fah, Vr))

# button
button = Pin(15, Pin.IN)

# LED
led = Pin(16, Pin.OUT)

while True:
    if button.value() == 0:
        print("You pressed the button!")
        led.value(1)
    else:
        led.value(0)

    utime.sleep(0.1)





