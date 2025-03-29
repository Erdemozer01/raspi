import gpiozero
from signal import pause


led = gpiozero.PWMLED(17)
try:
    led.pulse()
    pause()
except KeyboardInterrupt:
    print("Bye")


