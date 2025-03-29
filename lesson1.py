import time

from RPiSim.GPIO import GPIO
from gpiozero import LED
import gpiozero

led = LED(17)

while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
    gpiozero.Device.close_all()


