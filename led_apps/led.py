import gpiozero
from signal import pause
from time import sleep


def led_pulse(pin_number=None):
    led = gpiozero.PWMLED(pin_number)
    try:
        led.pulse()
        pause()
    except KeyboardInterrupt:
        led.close()
        pause()


def traffic_light(red_GPIO_number=None, yellow_GPIO_number=None, green_GPIO_number=None):
    lights = gpiozero.TrafficLights(red=red_GPIO_number, amber=yellow_GPIO_number, green=green_GPIO_number)

    lights.green.on()

    while True:
        sleep(10)
        lights.green.off()
        lights.amber.on()
        sleep(1)
        lights.amber.off()
        lights.red.on()
        sleep(10)
        lights.amber.on()
        sleep(1)
        lights.green.on()
        lights.amber.off()
        lights.red.off()
