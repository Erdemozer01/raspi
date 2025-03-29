import gpiozero
from signal import pause


def led(pin_number=None):
    led = gpiozero.PWMLED(pin_number)
    try:
        led.pulse()
        pause()
    except KeyboardInterrupt:
        gpiozero.Device.close()
        print("Bye")


led(17)