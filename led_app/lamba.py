from gpiozero import LEDBoard
from signal import pause

leds = LEDBoard(6, 13, 19, 26, pwm=True)

leds.value = (0.4, 0.6, 0.8, 1.0)

pause()