from gpiozero import DistanceSensor, LED
import time

# Ultrasonik Sensör Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

# LED Pinleri
RED_LED_PIN = 17
GREEN_LED_PIN = 18
YELLOW_LED_PIN = 27 # Sarı LED için yeni pin (GPIO27 olarak varsayıldı, uygun bir pin seçin)

try:
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2.0, queue_len=5)
except Exception as e:
    print(f"Sensör başlatma hatası: {e}")
    print("Lütfen pin bağlantılarını kontrol edin.")
    exit()

red_led = LED(RED_LED_PIN)
green_led = LED(GREEN_LED_PIN)
yellow_led = LED(YELLOW_LED_PIN)

THRESHOLD_CM = 10.0  # 10 cm

print("Ctrl+C ile programı sonlandırabilirsiniz.")

if __name__ == "__main__":
    try:
        # Başlangıç LED durumları
        green_led.off() # Başlangıçta yeşil kapalı
        red_led.off()
        yellow_led.off() # Başlangıçta sarı kapalı, ilk döngüde duruma göre ayarlanacak

        print("Mesafe ölçümü başlıyor...")

        while True:
            distance_m = sensor.distance
            distance_cm = distance_m * 100

            print(f"Mesafe: {distance_cm:.2f} cm")

            # Mesafe ölçümünün geçerli olup olmadığını kontrol et
            # 0.0 genellikle bir hata veya okuma yok anlamına gelir
            # sensor.max_distance değeri, nesnenin menzil dışında olduğunu gösterir
            is_reading_valid = (distance_m > 0.0) and (distance_m < sensor.max_distance)

            if is_reading_valid:
                # Geçerli mesafe ölçümü var: Sarı LED yanıp söner
                yellow_led.toggle()  # Sarı LED'i aç/kapa (yanıp sönme efekti)

                # Nesne yakınlık kontrolü
                is_object_detected_close = (distance_cm <= THRESHOLD_CM)

                if is_object_detected_close:
                    print("Nesne yakın! Kırmızı ışıkla uyarı veriliyor...")
                    red_led.on()
                    green_led.off()
                else:
                    print("Mesafe güvenli. Yeşil ışık yanıyor.")
                    green_led.on()
                    red_led.off()
            else:
                # Geçerli mesafe ölçümü yok: Sarı LED sürekli yanar, diğerleri söner
                print("Mesafe ölçümü yapılamıyor veya nesne menzil dışında. Sarı ışık sabit.")
                yellow_led.on()  # Sarı LED'i sürekli yak
                red_led.off()
                green_led.off()

            time.sleep(0.25)  # Yanıp sönme ve okuma aralığı için uygun bir süre

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")

    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

    finally:
        print("Pinler temizleniyor...")
        # Tüm LED'leri kapat ve kaynakları serbest bırak
        if 'red_led' in locals():
            if hasattr(red_led, 'is_active') and red_led.is_active:
                red_led.off()
            red_led.close()
        if 'green_led' in locals():
            if hasattr(green_led, 'is_active') and green_led.is_active:
                green_led.off()
            green_led.close()
        if 'yellow_led' in locals(): # Sarı LED için temizleme
            if hasattr(yellow_led, 'is_active') and yellow_led.is_active:
                yellow_led.off()
            yellow_led.close()

        if 'sensor' in locals() and hasattr(sensor, 'close'):
            sensor.close()

        print("Program sonlandı.")