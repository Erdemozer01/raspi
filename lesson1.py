import gpiozero
from signal import pause

try:

    led = gpiozero.PWMLED(17)
    while True:
        led.pulse()
except KeyboardInterrupt:
    pause()
