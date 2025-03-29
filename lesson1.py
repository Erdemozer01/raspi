import gpiozero
from signal import pause


def led(pin_number=None):
    led = gpiozero.PWMLED(pin_number)
    try:
        led.pulse()
        pause()
    except KeyboardInterrupt:
        led.close()



led(17)