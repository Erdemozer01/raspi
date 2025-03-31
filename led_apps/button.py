from gpiozero import Button, LED
from time import sleep
import random


def button():

    led = LED(17)

    player_1 = Button(2)
    player_2 = Button(3)

    time = random.uniform(5, 10)
    sleep(time)
    led.on()

    while True:
        if player_1.is_pressed:
            print("Player 1 wins!")
            break
        if player_2.is_pressed:
            print("Player 2 wins!")
            break

    led.off()


def button_led():
    from gpiozero import LED, Button
    from signal import pause

    led = LED(17)
    button = Button(2)

    button.when_pressed = led.on
    button.when_released = led.off

    pause()