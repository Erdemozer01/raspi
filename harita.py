from gpiozero import DistanceSensor, LED
import time
import math  # Harita çizimi için eklendi
# matplotlib'i kullanacaksanız ve kurulu değilse: sudo pip3 install matplotlib
import matplotlib.pyplot as plt  # Harita çizimi için eklendi (opsiyonel)

# Ultrasonik Sensör Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

# LED Pinleri
RED_LED_PIN = 17
GREEN_LED_PIN = 18
YELLOW_LED_PIN = 27

# Eşik Değerleri
OBJECT_THRESHOLD_CM = 20.0  # Kırmızı/Yeşil LED için nesne algılama eşiği (20 cm)
YELLOW_LED_THRESHOLD_CM = 100.0  # Sarı LED davranışı için eşik (100 cm)
TERMINATION_DISTANCE_CM = 10.0  # Program sonlandırma eşiği (10 cm'den az)

# Global değişkenler olarak tanımlayalım ki finally bloğunda erişilebilsin
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
    print(f"Donanım başlatma hatası (Sensör veya LED'ler): {e}")
    print("Lütfen pin bağlantılarını ve sudo yetkilerini kontrol edin.")
    exit()

harita_verileri = []  # Açı ve mesafe verilerini saklamak için liste

if __name__ == "__main__":
    try:
        # Başlangıç LED durumları
        red_led.off()
        green_led.off()
        yellow_led.off()

        print("Manuel Haritalama ve LED Kontrol Programı Başlatılıyor...")
        print(f"Kırmızı LED Eşiği: {OBJECT_THRESHOLD_CM} cm")
        print(f"Sarı LED Eşiği: {YELLOW_LED_THRESHOLD_CM} cm")
        print(f"Program Sonlandırma Mesafesi: < {TERMINATION_DISTANCE_CM} cm")
        print("----------------------------------------------------")
        print("Sensörü istediğiniz açıya getirin.")
        print("Her ölçüm için açıyı derece olarak girin veya çıkmak için 'q' yazın.")

        while True:
            try:
                aci_str = input("\nŞu anki açı (derece) veya 'q' (çıkış): ")
                if aci_str.lower() == 'q':
                    print("Çıkış komutu alındı.")
                    break

                aci_derece = float(aci_str)

                # 1. Mesafe Oku
                if sensor:  # Sensör başarıyla başlatıldıysa
                    distance_m = sensor.distance
                    distance_cm = distance_m * 100
                else:
                    print("HATA: Sensör bulunamadı/başlatılamadı!")
                    break  # Sensör yoksa döngüden çık

                print(f"-> Açı: {aci_derece}°, Okunan Mesafe: {distance_cm:.2f} cm")

                # 2. Haritalama Verisi Kaydet
                harita_verileri.append({'aci': aci_derece, 'mesafe_cm': distance_cm})

                # 3. Program Sonlandırma Kontrolü (< TERMINATION_DISTANCE_CM)
                if distance_cm < TERMINATION_DISTANCE_CM:
                    print(f"DİKKAT: Nesne çok yakın ({distance_cm:.2f}cm)! Güvenlik nedeniyle program sonlandırılıyor.")
                    # Son bir uyarı olarak tüm LED'leri kırmızı yapabiliriz (isteğe bağlı)
                    # red_led.on()
                    # green_led.off()
                    # yellow_led.off()
                    # time.sleep(1) # Kullanıcının görmesi için kısa bir bekleme
                    break  # Döngüyü sonlandır

                # 4. Sarı LED Mantığı
                if distance_cm > YELLOW_LED_THRESHOLD_CM:
                    yellow_led.on()
                    print("   Sarı LED: Sürekli Yanıyor (Mesafe > 100cm)")
                else:  # distance_cm <= YELLOW_LED_THRESHOLD_CM
                    yellow_led.toggle()  # Her adımda durumu değişir, yanıp sönme etkisi verir
                    print("   Sarı LED: Durumu Değişti (Yanıp Sönüyor olmalı, Mesafe <= 100cm)")

                # 5. Kırmızı/Yeşil LED Mantığı
                # is_reading_valid, sensörün 0 veya max_distance gibi sınır değerler döndürmediğini kontrol eder.
                # max_distance_cm burada sensörün maksimum okuma yapabildiği cm cinsinden değerdir.
                max_distance_cm = sensor.max_distance * 100
                is_reading_valid = (distance_cm > 0.0) and (distance_cm < max_distance_cm)

                if is_reading_valid:
                    if distance_cm <= OBJECT_THRESHOLD_CM:
                        print(
                            f"   Kırmızı/Yeşil: Nesne Yakın ({distance_cm:.2f}cm <= {OBJECT_THRESHOLD_CM:.0f}cm)! Kırmızı LED Aktif.")
                        red_led.on()
                        green_led.off()
                    else:
                        print(
                            f"   Kırmızı/Yeşil: Mesafe Güvenli ({distance_cm:.2f}cm > {OBJECT_THRESHOLD_CM:.0f}cm). Yeşil LED Aktif.")
                        green_led.on()
                        red_led.off()
                else:
                    status_message = "   Kırmızı/Yeşil LEDler: Kapalı (Sensör "
                    if distance_cm == 0.0:
                        status_message += "0.0cm okuyor - çok yakın veya hata)."
                    elif distance_cm >= max_distance_cm:  # Eşitlik durumu da menzil dışı sayılır
                        status_message += f"menzil dışında >= {max_distance_cm:.0f}cm)."
                    else:  # Bu durum normalde oluşmamalı
                        status_message += "tanımsız bir sınır değer okuyor)."
                    print(status_message)
                    red_led.off()
                    green_led.off()

            except ValueError:
                print("Geçersiz açı girdiniz. Lütfen sayısal bir değer (örn: 45) veya 'q' girin.")
            except Exception as e_loop:
                print(f"Döngü içinde bir hata oluştu: {e_loop}")
                # Hata durumunda devam etmeyi veya çıkmayı seçebilirsiniz
                # break # Ciddi bir hataysa döngüden çık
                pass  # Küçük hatalarda devam etmeye çalış

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından (Ctrl+C) sonlandırıldı.")
    except Exception as e_main:
        print(f"Programda genel bir hata oluştu: {e_main}")

    finally:
        print("\n--- Haritalama Verileri Sonucu ---")
        if not harita_verileri:
            print("Hiç harita verisi toplanmadı.")
        else:
            print(f"Toplam {len(harita_verileri)} nokta kaydedildi:")
            for i, veri in enumerate(harita_verileri):
                print(f"  {i + 1}. Açı: {veri['aci']}°, Mesafe: {veri['mesafe_cm']:.2f} cm")

            # Matplotlib ile çizim (opsiyonel)
            # Eğer Raspberry Pi'de grafik arayüzü yoksa veya matplotlib kurulu değilse bu kısım hata verebilir.
            # Bu yüzden try-except bloğu içine almak iyi bir fikirdir.
            print("\nHarita çizdirme denemesi (matplotlib gerektirir)...")
            try:
                if not harita_verileri:  # Tekrar kontrol, yukarıda da var ama garanti olsun
                    raise ValueError("Çizilecek veri yok.")

                noktalar_x = []
                noktalar_y = []
                # Sensörün kendi maksimum mesafesini alalım
                sensor_max_range_cm = sensor.max_distance * 100 if sensor else 200  # Varsayılan 200cm

                for veri in harita_verileri:
                    # Sadece "geçerli" ve "anlamlı" ölçümleri çizdirelim
                    # (0'dan büyük ve sensörün maksimum menzilinden küçük)
                    if 0 < veri['mesafe_cm'] < sensor_max_range_cm:
                        aci_radyan = math.radians(float(veri['aci']))  # Açıyı float yapmayı unutma
                        x = veri['mesafe_cm'] * math.cos(aci_radyan)
                        y = veri['mesafe_cm'] * math.sin(aci_radyan)
                        noktalar_x.append(x)
                        noktalar_y.append(y)

                if noktalar_x:  # Eğer çizdirilecek geçerli nokta varsa
                    plt.figure(figsize=(10, 10))
                    plt.scatter(noktalar_x, noktalar_y, color='blue', label='Algılanan Noktalar')
                    plt.plot(0, 0, 'ro', markersize=10, label='Sensör Konumu')  # Sensörün merkezi
                    plt.title("Manuel Taranmış 2D Harita (Sensör Merkezli)")
                    plt.xlabel("X Ekseni (cm)")
                    plt.ylabel("Y Ekseni (cm)")
                    plt.axhline(0, color='grey', lw=0.5)
                    plt.axvline(0, color='grey', lw=0.5)
                    plt.axis('equal')  # Eksenleri eşit ölçeklendir
                    plt.grid(True)
                    plt.legend()
                    plt.savefig("haritam.png") # İsterseniz dosyaya kaydedebilirsiniz
                    plt.show()  # Grafiği göster
                else:
                    print("Çizdirilecek geçerli harita noktası bulunamadı (tüm ölçümler 0 veya menzil dışı olabilir).")

            except ImportError:
                print("Matplotlib kütüphanesi kurulu değil veya bulunamadı. Harita çizilemedi.")
                print("Kurmak için: sudo pip3 install matplotlib")
            except ValueError as ve:
                print(f"Çizim için veri hatası: {ve}")
            except Exception as e_plot:
                print(f"Harita çizimi sırasında bir hata oluştu: {e_plot}")

        print("\nPinler temizleniyor...")
        if red_led and hasattr(red_led, 'close'):
            if hasattr(red_led, 'is_active') and red_led.is_active: red_led.off()
            red_led.close()
        if green_led and hasattr(green_led, 'close'):
            if hasattr(green_led, 'is_active') and green_led.is_active: green_led.off()
            green_led.close()
        if yellow_led and hasattr(yellow_led, 'close'):
            if hasattr(yellow_led, 'is_active') and yellow_led.is_active: yellow_led.off()
            yellow_led.close()

        if sensor and hasattr(sensor, 'close'):
            sensor.close()

        print("Program başarıyla sonlandı.")