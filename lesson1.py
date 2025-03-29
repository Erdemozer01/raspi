import time
import gpiozero

led = gpiozero.LED(17)

try:
    while True:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
except:
    gpiozero.GPIODevice.close()
