from led_apps import led

title = "*"*50 + "\n" + "İşlem Seçiniz" + "\n" + "1 - Pulse Kontrol" + "\n" + "2 - Traffic Lights"+ "\n" + "*"*50


while True:

    choice_app = int(input(title))

    if choice_app is not int:

        print("Hatalı Şeçim")

        continue

    if choice_app == 1:

        pin_number = int(input("Pin Number: "))

        try:
            led.led_pulse(pin_number=pin_number)
        except:
            print("Pin numarasını doğru yazdığınızdan emin olun")
            continue
