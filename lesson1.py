from gpio import output
import time
import  gpiozero

led = gpiozero.LED(17)

while True:
    led.on()
    time.sleep(1)
    led.off()

