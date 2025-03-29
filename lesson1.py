import time
import gpiozero
from signal import pause

def led_signal():
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)


try:
    led = gpiozero.LED(17)
    led_signal()

except:
    pause()
    led_signal()

