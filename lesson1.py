import gpiozero
from signal import pause

led = gpiozero.PWMLED(17)

led.blink()

led.pulse()

pause()