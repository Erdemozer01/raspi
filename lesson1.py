from time import sleep
import gpiozero
from signal import pause


led = gpiozero.LED(17)

led.blink()

pause()