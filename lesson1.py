import time
import gpiozero
from signal import pause



try:
    led = gpiozero.LED(17)
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

except:
    pause()
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

