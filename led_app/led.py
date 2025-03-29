import gpiozero
from signal import pause


def led_pulse(pin_number=None):
    led = gpiozero.PWMLED(pin_number)
    try:
        led.pulse()
        pause()
    except KeyboardInterrupt:
        led.close()


led_pulse(17)