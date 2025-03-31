from led_apps import led, button

title = "*" * 50 + "\n" + "Uygulamalar" + "\n" + "1 - Pulse Kontrol" + "\n" + "2 - Traffic Lights" + "\n" + "3 - Button game" + "\n" + "3 - Button kontrol" + "\n" + "*" * 50 + "\n\n"

print(title)

while True:

    choice_app = int(input("Islem : "))

    if choice_app == 1:

        pin_number = int(input("Pin: "))

        try:

            led.led_pulse(pin_number=pin_number)

        except:

            print("Pin numarasini kontrol edin")

            pass

    elif choice_app == 2:

        try:

            red = int(input("Kirmizi: "))
            yellow = int(input("Sari: "))
            green = int(input("Yesil: "))

            led.traffic_light(red_GPIO_number=red, yellow_GPIO_number=yellow, green_GPIO_number=green)

        except:

            print("Pin numarasini kontrol edin")
            pass

    elif choice_app == 3:

        try:

            button.button()

        except:

            print("Pin numarasini kontrol edin")
            pass
