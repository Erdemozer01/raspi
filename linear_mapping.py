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

# Global değişkenler
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
    print(f"Donanım başlatma hatası: {e}")
    print("Lütfen pin bağlantılarını ve sudo yetkilerini kontrol edin.")
    exit()

# Haritalama için veri listesi ve örnek sayacı
harita_verileri_otonom = []
ornek_sayaci = 0

print("Ctrl+C ile programı sonlandırabilirsiniz.")

if __name__ == "__main__":
    try:
        # Başlangıç LED durumları
        if red_led: red_led.off()
        if green_led: green_led.off()
        if yellow_led: yellow_led.off()

        print("Otonom Mesafe Ölçümü ve Veri Kaydı Başlıyor...")
        print(f"Veriler {time.sleep.__name__} ({0.25} sn) aralıklarla kaydedilecek.")  # time.sleep süresini belirtelim
        print(f"Kırmızı LED Eşiği: {OBJECT_THRESHOLD_CM} cm")
        print(f"Sarı LED Eşiği: {YELLOW_LED_THRESHOLD_CM} cm")
        print(f"Program Sonlandırma Mesafesi: < {TERMINATION_DISTANCE_CM} cm")
        print("----------------------------------------------------")

        while True:
            if not sensor:  # Güvenlik kontrolü
                print("HATA: Sensör düzgün başlatılamamış!")
                break
            distance_m = sensor.distance
            distance_cm = distance_m * 100

            print(f"Örnek No: {ornek_sayaci}, Mesafe: {distance_cm:.2f} cm")

            # Veri Kaydı
            harita_verileri_otonom.append({'ornek_no': ornek_sayaci, 'mesafe_cm': distance_cm})
            ornek_sayaci += 1

            # 1. Program Sonlandırma Kontrolü
            if distance_cm < TERMINATION_DISTANCE_CM:
                print(f"DİKKAT: Nesne çok yakın ({distance_cm:.2f}cm)! Güvenlik nedeniyle program sonlandırılıyor.")
                break  # Döngüyü sonlandır ve finally bloğuna git

            # 2. Sarı LED Mantığı
            if distance_cm > YELLOW_LED_THRESHOLD_CM:
                yellow_led.on()
                # print("Sarı LED: Sürekli Yanıyor (Mesafe > 100cm)") # İsteğe bağlı detaylı log
            else:  # distance_cm <= YELLOW_LED_THRESHOLD_CM (0 cm dahil)
                yellow_led.toggle()
                # print("Sarı LED: Yanıp Sönüyor (Mesafe <= 100cm)") # İsteğe bağlı

            # 3. Kırmızı/Yeşil LED Mantığı
            max_distance_cm = sensor.max_distance * 100
            is_reading_valid = (distance_cm > 0.0) and (distance_cm < max_distance_cm)

            if is_reading_valid:
                if distance_cm <= OBJECT_THRESHOLD_CM:
                    # print(f"Kırmızı/Yeşil: Nesne Yakın ({distance_cm:.2f}cm <= {OBJECT_THRESHOLD_CM:.0f}cm)! Kırmızı LED Aktif.") # İsteğe bağlı
                    red_led.on()
                    green_led.off()
                else:
                    # print(f"Kırmızı/Yeşil: Mesafe Güvenli ({distance_cm:.2f}cm > {OBJECT_THRESHOLD_CM:.0f}cm). Yeşil LED Aktif.") # İsteğe bağlı
                    green_led.on()
                    red_led.off()
            else:
                # status_message = "Kırmızı/Yeşil LEDler: Kapalı (Sensör " # İsteğe bağlı
                # if distance_cm == 0.0:
                #     status_message += "0.0cm okuyor)."
                # elif distance_cm >= max_distance_cm:
                #     status_message += f"max menzilde ({max_distance_cm:.0f}cm) okuyor)."
                # else:
                #     status_message += "geçersiz bir değer okuyor)."
                # print(status_message) # İsteğe bağlı
                red_led.off()
                green_led.off()

            time.sleep(0.25)  # Otonom ölçüm aralığı

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından (Ctrl+C) sonlandırıldı.")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

    finally:
        print("\n--- Otonom Ölçüm Verileri (Lineer Model Haritası) ---")
        if not harita_verileri_otonom:
            print("Hiç veri toplanmadı.")
        else:
            print(f"Toplam {len(harita_verileri_otonom)} ölçüm kaydedildi:")
            # İsteğe bağlı olarak ilk ve son birkaç veriyi gösterebilirsiniz
            # for i, veri in enumerate(harita_verileri_otonom[:5]): # İlk 5
            #     print(f"  {veri['ornek_no']}. Mesafe: {veri['mesafe_cm']:.2f} cm")
            # if len(harita_verileri_otonom) > 5: print("  ...")

            print("\nHarita/Profil çizdirme denemesi (matplotlib gerektirir)...")
            try:
                if not harita_verileri_otonom:
                    raise ValueError("Çizilecek veri yok.")

                ornek_numaralari = [veri['ornek_no'] for veri in harita_verileri_otonom]
                mesafeler = [veri['mesafe_cm'] for veri in harita_verileri_otonom]

                plt.figure(figsize=(12, 7))
                plt.plot(ornek_numaralari, mesafeler, marker='.', linestyle='-', color='slateblue',
                         label='Ölçülen Mesafe')

                plt.title("Sıralı Mesafe Ölçümleri Profili (Otonom Kayıt)")
                plt.xlabel("Örnek Numarası (Zamanla Artan)")
                plt.ylabel("Ölçülen Mesafe (cm)")
                plt.legend()
                plt.grid(True)
                plt.ylim(bottom=0)
                plt.savefig("otonom_mesafe_profili.png") # İsterseniz dosyaya kaydedebilirsiniz
                plt.show()

            except ImportError:
                print("Matplotlib kütüphanesi kurulu değil veya bulunamadı. Harita çizilemedi.")
                print("Kurmak için: sudo pip3 install matplotlib")
            except ValueError as ve:
                print(f"Çizim için veri hatası: {ve}")
            except Exception as e_plot:
                print(f"Harita çizimi sırasında bir hata oluştu: {e_plot}")

        print("\nPinler temizleniyor...")
        # Pin temizleme (önceki kodunuzdaki gibi, None kontrolleri eklendi)
        if 'red_led' in locals() and red_led is not None:
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