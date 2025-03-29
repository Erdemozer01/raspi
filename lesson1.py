import time
import gpiozero
from signal import pause

led = gpiozero.LED(17)

try:
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
except:
    led.source = 0
