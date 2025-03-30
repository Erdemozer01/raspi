from led_apps import led

title = "*"*50 + "\n" + "Uygulamalar" + "\n" + "1 - Pulse Kontrol" + "\n" + "2 - Traffic Lights"+ "\n" + "*"*50 + "\n\n"


while True:

    choice_app = int(input("Islem : "))

    if choice_app == 1:

        pin_number = int(input("Pin: "))

        try:
            led.led_pulse(pin_number=pin_number)
        except:
            print("Pin numarasını doğru yazdığınızdan emin olun")
            pass
    elif choice_app == 2:
        try:
            red = int(input("Kirmizi: "))
            yellow = int(input("Sari: "))
            green = int(input("Yesil: "))

            led.traffic_light(red_pin_number=red, green_pin_number=green, yellow_pin_number=yellow)

        except:
            print("Pin numarasını doğru yazdığınızdan emin olun")
            pass
