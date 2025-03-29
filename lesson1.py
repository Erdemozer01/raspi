import gpiozero
from signal import pause

led = gpiozero.PWMLED(17)

led.pulse()

pause()