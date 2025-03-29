import time
import gpiozero
from signal import pause

from gpiozero import LEDBoard

led = gpiozero.LED(17)

try:
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
except:
    tree = LEDBoard(*range(2, 28), pwm=True)
    for led in tree:
        led.source = 0
    tree.off()
