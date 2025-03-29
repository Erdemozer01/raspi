import gpiozero
from signal import pause

try:
    led = gpiozero.PWMLED(17)

    led.pulse()
except KeyboardInterrupt:
    pause()
