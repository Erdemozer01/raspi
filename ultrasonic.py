from gpiozero import DistanceSensor, LED
import time

# Ultrasonic Sensor Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

RED_LED_PIN = 17
GREEN_LED_PIN = 18

try:
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2.0, queue_len=5)
except Exception as e:
    print(f"Hata meydana geldi: {e}")
    print("Lütfen kotrol edin")
    exit()

red_led = LED(RED_LED_PIN)
green_led = LED(GREEN_LED_PIN)

THRESHOLD_CM = 10.0  # 10 cm

print("Press Ctrl+C ile programdan çık.")

if __name__ == "__main__":
    try:

        green_led.on()
        red_led.off()

        while True:
            distance_m = sensor.distance
            distance_cm = distance_m * 100

            print(f"Mesafe: {distance_cm:.2f} cm")

            is_object_detected_close_and_valid = (0 < distance_cm <= THRESHOLD_CM) and \
                                                 (distance_m != 0.0) and \
                                                 (distance_m != sensor.max_distance)

            if is_object_detected_close_and_valid:

                print("Nesne tespit edildi dur. Kırmızı ısıgı yak....")

                red_led.on()
                green_led.off()

            else:
                print("Rahat hareket et, Yeşil ışığı yak")

                green_led.on()
                red_led.off()

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nProgram sonlandı.")

    except Exception as e:
        print(f"Beklenmedik hata: {e}")

    finally:

        print("Pinler temizleniyor...")
        # Turn off all LEDs and close resources
        if 'red_led' in locals():
            if hasattr(red_led, 'is_active') and red_led.is_active: red_led.off()
            red_led.close()
        if 'green_led' in locals():
            if hasattr(green_led, 'is_active') and green_led.is_active: green_led.off()
            green_led.close()

        if 'sensor' in locals() and hasattr(sensor, 'close'):
            sensor.close()


