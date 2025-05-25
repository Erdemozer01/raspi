from gpiozero import DistanceSensor, LED
import time
import matplotlib.pyplot as plt  # Harita çizimi için eklendi

# Ultrasonik Sensör Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

# LED Pinleri
RED_LED_PIN = 17
GREEN_LED_PIN = 18
YELLOW_LED_PIN = 27

# Eşik Değerleri
OBJECT_THRESHOLD_CM = 20.0  # Kırmızı/Yeşil LED için nesne algılama eşiği
YELLOW_LED_THRESHOLD_CM = 100.0  # Sarı LED davranışı için eşik
TERMINATION_DISTANCE_CM = 10.0  # Program sonlandırma eşiği (10 cm'den az)

# Global değişkenler (önceki kodunuzdaki gibi)
sensor = None
red_led = None
green_led = None
yellow_led = None

try:
    sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, max_distance=2.0, queue_len=5)
    red_led = LED(RED_LED_PIN)
    green_led = LED(GREEN_LED_PIN)
    yellow_led = LED(YELLOW_LED_PIN)
except Exception as e:
    print(f"Donanım başlatma hatası: {e}")  # Hata mesajı güncellendi
    print("Lütfen pin bağlantılarını ve sudo yetkilerini kontrol edin.")
    exit()

harita_verileri_1d = []  # (Pozisyon, Mesafe) verilerini saklamak için liste

print("Ctrl+C ile programı sonlandırabilirsiniz.")  # Bu mesaj __main__ dışına alındı, genel bilgi

if __name__ == "__main__":
    try:
        # Başlangıç LED durumları
        if red_led: red_led.off()
        if green_led: green_led.off()
        if yellow_led: yellow_led.off()

        print("Manuel 1D Lineer Haritalama (Ultrasonik Sensör ile) Başlatılıyor...")
        print(f"Kırmızı LED Eşiği: {OBJECT_THRESHOLD_CM} cm")
        print(f"Sarı LED Eşiği: {YELLOW_LED_THRESHOLD_CM} cm")
        print(f"Program Sonlandırma Mesafesi (Ölçülen): < {TERMINATION_DISTANCE_CM} cm")
        print("----------------------------------------------------")
        print("Sensörü lineer yol üzerindeki bir sonraki konuma getirin.")
        print("Her ölçüm için, sensörün başlangıç noktasına olan uzaklığını cm olarak girin.")
        print("Çıkmak için pozisyon yerine 'q' yazın.")

        while True:
            try:
                pozisyon_str = input("\nSensörün şu anki pozisyonu (cm) veya 'q' (çıkış): ")
                if pozisyon_str.lower() == 'q':
                    print("Çıkış komutu alındı.")
                    break

                pozisyon_cm_input = float(pozisyon_str)

                # Mesafe Oku
                if not sensor:  # Güvenlik kontrolü
                    print("HATA: Sensör düzgün başlatılamamış!")
                    break
                distance_m = sensor.distance
                distance_cm = distance_m * 100

                print(f"-> Pozisyon: {pozisyon_cm_input:.1f} cm, Ölçülen Mesafe: {distance_cm:.2f} cm")

                # Haritalama Verisi Kaydet
                harita_verileri_1d.append({'pozisyon_cm': pozisyon_cm_input, 'mesafe_cm': distance_cm})

                # 1. Program Sonlandırma Kontrolü (Ölçülen mesafeye göre)
                if distance_cm < TERMINATION_DISTANCE_CM:
                    print(f"DİKKAT: Engel çok yakın ({distance_cm:.2f}cm)! Güvenlik nedeniyle program sonlandırılıyor.")
                    break  # Döngüyü sonlandır ve finally bloğuna git

                # 2. Sarı LED Mantığı (Ölçülen mesafeye göre)
                if distance_cm > YELLOW_LED_THRESHOLD_CM:
                    yellow_led.on()
                    print("   Sarı LED: Sürekli Yanıyor (Ölçülen Mesafe > 100cm)")
                else:  # distance_cm <= YELLOW_LED_THRESHOLD_CM (0 cm dahil)
                    yellow_led.toggle()
                    print("   Sarı LED: Durumu Değişti (Yanıp Sönüyor olmalı, Ölçülen Mesafe <= 100cm)")

                # 3. Kırmızı/Yeşil LED Mantığı (Ölçülen mesafeye göre)
                # max_distance_cm burada sensörün maksimum okuma yapabildiği cm cinsinden değerdir.
                max_distance_cm = sensor.max_distance * 100
                is_reading_valid = (distance_cm > 0.0) and (distance_cm < max_distance_cm)  # distance_cm kullanılır

                if is_reading_valid:
                    if distance_cm <= OBJECT_THRESHOLD_CM:
                        print(
                            f"   Kırmızı/Yeşil: Engel Yakın ({distance_cm:.2f}cm <= {OBJECT_THRESHOLD_CM:.0f}cm)! Kırmızı LED Aktif.")
                        red_led.on()
                        green_led.off()
                    else:
                        print(
                            f"   Kırmızı/Yeşil: Mesafe Güvenli ({distance_cm:.2f}cm > {OBJECT_THRESHOLD_CM:.0f}cm). Yeşil LED Aktif.")
                        green_led.on()
                        red_led.off()
                else:
                    status_message = "   Kırmızı/Yeşil LEDler: Kapalı (Sensör "
                    if distance_cm == 0.0:  # distance_m yerine distance_cm
                        status_message += "0.0cm okuyor - çok yakın veya hata)."
                    elif distance_cm >= max_distance_cm:  # distance_m yerine distance_cm
                        status_message += f"menzil dışında >= {max_distance_cm:.0f}cm)."
                    else:
                        status_message += "tanımsız bir sınır değer okuyor)."
                    print(status_message)
                    red_led.off()
                    green_led.off()

                # time.sleep(0.25) # Kullanıcı girişi zaten döngüyü yavaşlatacağı için bu satıra gerek yok.

            except ValueError:
                print("Geçersiz pozisyon girdiniz. Lütfen sayısal bir değer (örn: 15.5) veya 'q' girin.")
            except Exception as e_loop:  # Döngü içindeki diğer hatalar için
                print(f"Döngü içinde bir hata oluştu: {e_loop}")
                pass  # Hata durumunda bir sonraki adıma geçmeye çalış

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından (Ctrl+C) sonlandırıldı.")
    except Exception as e_main:  # Daha genel hatalar için
        print(f"Programda genel bir hata oluştu: {e_main}")

    finally:
        print("\n--- 1D Lineer Haritalama Verileri Sonucu (Ultrasonik) ---")
        if not harita_verileri_1d:
            print("Hiç harita verisi toplanmadı.")
        else:
            print(f"Toplam {len(harita_verileri_1d)} nokta kaydedildi:")
            for i, veri in enumerate(harita_verileri_1d):
                print(
                    f"  {i + 1}. Sensör Pozisyonu: {veri['pozisyon_cm']:.1f} cm, Ölçülen Mesafe: {veri['mesafe_cm']:.2f} cm")

            print("\n1D Harita/Profil çizdirme denemesi (matplotlib gerektirir)...")
            try:
                if not harita_verileri_1d:
                    raise ValueError("Çizilecek veri yok.")

                pozisyonlar = [veri['pozisyon_cm'] for veri in harita_verileri_1d]
                mesafeler = [veri['mesafe_cm'] for veri in harita_verileri_1d]

                plt.figure(figsize=(12, 7))
                plt.plot(pozisyonlar, mesafeler, marker='o', linestyle='-', color='dodgerblue',
                         label='Ölçülen Mesafe Profili')

                plt.title("Manuel 1D Lineer Tarama Profili (Ultrasonik Sensör ile)")
                plt.xlabel("Sensörün Hat Üzerindeki Pozisyonu (cm)")
                plt.ylabel("Ölçülen Mesafe (cm)")
                plt.legend()
                plt.grid(True)
                plt.ylim(bottom=0)
                # plt.savefig("1d_ultrasonik_haritam.png") # İsterseniz dosyaya kaydedebilirsiniz
                plt.show()

            except ImportError:
                print("Matplotlib kütüphanesi kurulu değil veya bulunamadı. Harita çizilemedi.")
                print("Kurmak için: sudo pip3 install matplotlib")
            except ValueError as ve:  # Özellikle "Çizilecek veri yok" durumu için
                print(f"Çizim için veri hatası: {ve}")
            except Exception as e_plot:  # Diğer olası çizim hataları
                print(f"Harita çizimi sırasında bir hata oluştu: {e_plot}")

        print("\nPinler temizleniyor...")
        # Önceki kodunuzdaki pin temizleme mantığı korunuyor
        if 'red_led' in locals() and red_led is not None:  # Ekstra None kontrolü
            if hasattr(red_led, 'is_active') and red_led.is_active: red_led.off()
            if hasattr(red_led, 'close'): red_led.close()
        if 'green_led' in locals() and green_led is not None:
            if hasattr(green_led, 'is_active') and green_led.is_active: green_led.off()
            if hasattr(green_led, 'close'): green_led.close()
        if 'yellow_led' in locals() and yellow_led is not None:
            if hasattr(yellow_led, 'is_active') and yellow_led.is_active: yellow_led.off()
            if hasattr(yellow_led, 'close'): yellow_led.close()

        if 'sensor' in locals() and sensor is not None:
            if hasattr(sensor, 'close'): sensor.close()

        print("Program başarıyla sonlandı.")