import math
from machine import ADC

def read_temp(thermistor: ADC):
    temperature_value = thermistor.read_u16()
    Vr = 3.3 * float(temperature_value) / 65535
    Rt = 10000 * Vr / (3.3 - Vr)
    temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32
    return Cel, Fah
