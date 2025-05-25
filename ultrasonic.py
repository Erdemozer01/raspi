from gpiozero import DistanceSensor, LED
import time

# Ultrasonik Sensör Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

# LED Pinleri
RED_LED_PIN = 17
GREEN_LED_PIN = 18
YELLOW_LED_PIN = 27 # Sarı LED için GPIO27 kullanılıyor, gerekirse değiştirin

# Eşik Değerleri
OBJECT_THRESHOLD_CM = 20.0  # Kırmızı/Yeşil LED için nesne algılama eşiği (10 cm)
YELLOW_LED_THRESHOLD_CM = 100.0 # Sarı LED davranışı için eşik (100 cm)

try:
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2.0, queue_len=5)
except Exception as e:
    print(f"Sensör başlatma hatası: {e}")
    print("Lütfen pin bağlantılarını kontrol edin.")
    exit()

red_led = LED(RED_LED_PIN)
green_led = LED(GREEN_LED_PIN)
yellow_led = LED(YELLOW_LED_PIN)

print("Ctrl+C ile programı sonlandırabilirsiniz.")

if __name__ == "__main__":
    try:
        # Başlangıç LED durumları
        red_led.off()
        green_led.off()
        yellow_led.off() # Sarı LED döngü içinde durumuna göre ayarlanacak

        print("Mesafe ölçümü başlıyor...")

        while True:
            distance_m = sensor.distance
            distance_cm = distance_m * 100

            print(f"Mesafe: {distance_cm:.2f} cm")

            # 1. Sarı LED Mantığı (Yeni Kural)
            if distance_cm > YELLOW_LED_THRESHOLD_CM:
                yellow_led.on()
                print("Sarı LED: Sürekli Yanıyor (Mesafe > 100cm)")
            else:  # distance_cm <= YELLOW_LED_THRESHOLD_CM (0 cm dahil)
                yellow_led.toggle()
                print("Sarı LED: Yanıp Sönüyor (Mesafe <= 100cm)")

            # 2. Kırmızı/Yeşil LED Mantığı (Önceki gibi, geçerli okumaya bağlı)
            # 'is_reading_valid' kontrolü, sensörün 0 veya max_distance gibi
            # sınır değerler döndürmediğinden emin olmak içindir.
            is_reading_valid = (distance_m > 0.0) and (distance_m < sensor.max_distance)

            if is_reading_valid:
                if distance_cm <= OBJECT_THRESHOLD_CM:  # Nesne 10 cm veya daha yakınsa
                    print(f"Kırmızı/Yeşil: Nesne Çok Yakın ({distance_cm:.2f}cm)! Kırmızı LED Aktif.")
                    red_led.on()
                    green_led.off()
                else: # Nesne 10 cm'den uzaktaysa (ama hala geçerli bir okuma)
                    print(f"Kırmızı/Yeşil: Mesafe Güvenli ({distance_cm:.2f}cm). Yeşil LED Aktif.")
                    green_led.on()
                    red_led.off()
            else:
                # Geçersiz okuma durumunda (0.0m veya sensörün max_distance değeri),
                # kırmızı ve yeşil LED'ler kapatılır. Sarı LED'in davranışı yukarıda zaten belirlendi.
                status_message = "Kırmızı/Yeşil LEDler: Kapalı (Sensör "
                if distance_m == 0.0:
                    status_message += "0.0m okuyor)."
                elif distance_m == sensor.max_distance:
                    status_message += f"max menzilde ({sensor.max_distance*100:.0f}cm) okuyor)."
                else: # Bu durum normalde oluşmamalı
                    status_message += "geçersiz bir değer okuyor)."
                print(status_message)
                red_led.off()
                green_led.off()

            time.sleep(0.25)  # Yanıp sönme hızı ve okuma aralığı

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")

    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

    finally:
        print("Pinler temizleniyor...")
        # Tüm LED'leri kapat ve kaynakları serbest bırak
        if 'red_led' in locals():
            if hasattr(red_led, 'is_active') and red_led.is_active: red_led.off()
            red_led.close()
        if 'green_led' in locals():
            if hasattr(green_led, 'is_active') and green_led.is_active: green_led.off()
            green_led.close()
        if 'yellow_led' in locals():
            if hasattr(yellow_led, 'is_active') and yellow_led.is_active: yellow_led.off()
            yellow_led.close()
        if 'sensor' in locals() and hasattr(sensor, 'close'):
            sensor.close()
        print("Program sonlandı.")