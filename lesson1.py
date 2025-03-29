import time
import gpiozero
from signal import pause

from RPiSim.GPIO import GPIO

led = gpiozero.LED(17)

try:
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
except:
    gpiozero.LED.close(led)
