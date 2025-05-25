from gpiozero import DistanceSensor, LED
import time
import matplotlib.pyplot as plt  # Harita çizimi için eklendi
import numpy as np  # Ortalama gibi hesaplamalar için (opsiyonel, sum/len de yeterli)

# Ultrasonik Sensör Pinleri
TRIG_PIN = 23
ECHO_PIN = 24

# LED Pinleri
RED_LED_PIN = 17
GREEN_LED_PIN = 18
YELLOW_LED_PIN = 27

# Eşik Değerleri
OBJECT_THRESHOLD_CM = 20.0
YELLOW_LED_THRESHOLD_CM = 100.0
TERMINATION_DISTANCE_CM = 10.0
DELTA_T_SECONDS = 0.25  # time.sleep(0.25) ile uyumlu zaman aralığı

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
        if red_led: red_led.off()
        if green_led: green_led.off()
        if yellow_led: yellow_led.off()

        print("Otonom Mesafe Ölçümü, Veri Kaydı ve Hız Tahmini Başlıyor...")
        print(f"Veriler yaklaşık {DELTA_T_SECONDS} saniye aralıklarla kaydedilecek.")
        print("----------------------------------------------------")

        while True:
            if not sensor:
                print("HATA: Sensör düzgün başlatılamamış!")
                break

            start_time_loop = time.time()  # Gerçek zaman aralığını ölçmek için (opsiyonel, daha hassas)

            distance_m = sensor.distance
            distance_cm = distance_m * 100

            print(f"Örnek No: {ornek_sayaci}, Mesafe: {distance_cm:.2f} cm")

            harita_verileri_otonom.append({
                'ornek_no': ornek_sayaci,
                'mesafe_cm': distance_cm,
                'zaman_s': time.time()  # Her örneğin zaman damgasını da kaydedelim
            })
            ornek_sayaci += 1

            if distance_cm < TERMINATION_DISTANCE_CM:
                print(f"DİKKAT: Nesne çok yakın ({distance_cm:.2f}cm)! Güvenlik nedeniyle program sonlandırılıyor.")
                break

            if distance_cm > YELLOW_LED_THRESHOLD_CM:
                yellow_led.on()
            else:
                yellow_led.toggle()

            max_distance_cm = sensor.max_distance * 100
            is_reading_valid = (distance_cm > 0.0) and (distance_cm < max_distance_cm)

            if is_reading_valid:
                if distance_cm <= OBJECT_THRESHOLD_CM:
                    red_led.on()
                    green_led.off()
                else:
                    green_led.on()
                    red_led.off()
            else:
                red_led.off()
                green_led.off()

            # Döngüdeki işlemlerin süresini hesaba katarak DELTA_T_SECONDS'ı tamamla
            loop_processing_time = time.time() - start_time_loop
            sleep_time = DELTA_T_SECONDS - loop_processing_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından (Ctrl+C) sonlandırıldı.")
    except Exception as e:
        print(f"Beklenmedik bir hata oluştu: {e}")

    finally:
        print("\n--- Otonom Ölçüm Verileri ve Tahminler ---")

        # Hız Hesaplama ve Mesafe İstatistikleri
        if len(harita_verileri_otonom) > 0:
            # Hızları hesapla
            for i in range(len(harita_verileri_otonom)):
                if i == 0:
                    harita_verileri_otonom[i]['hiz_cm_s'] = 0.0  # İlk örnek için hız 0
                else:
                    delta_distance_cm = harita_verileri_otonom[i]['mesafe_cm'] - harita_verileri_otonom[i - 1][
                        'mesafe_cm']
                    # Gerçek zaman farkını kullan (daha hassas)
                    delta_t_actual = harita_verileri_otonom[i]['zaman_s'] - harita_verileri_otonom[i - 1]['zaman_s']
                    if delta_t_actual > 0:  # Sıfıra bölme hatasını engelle
                        harita_verileri_otonom[i]['hiz_cm_s'] = delta_distance_cm / delta_t_actual
                    else:  # Çok hızlı örnekleme durumunda (pratikte zor)
                        harita_verileri_otonom[i]['hiz_cm_s'] = 0.0

            print(f"Toplam {len(harita_verileri_otonom)} ölçüm kaydedildi:")
            for veri in harita_verileri_otonom:
                hiz_str = f"{veri['hiz_cm_s']:.2f}" if 'hiz_cm_s' in veri else "N/A"
                print(
                    f"  Örnek No: {veri['ornek_no']}, Mesafe: {veri['mesafe_cm']:.2f} cm, Tahmini Hız: {hiz_str} cm/s")

            all_distances = [d['mesafe_cm'] for d in harita_verileri_otonom]
            min_dist = min(all_distances)
            max_dist = max(all_distances)
            avg_dist = sum(all_distances) / len(all_distances)
            print(f"\nMesafe İstatistikleri:")
            print(f"  Minimum Mesafe: {min_dist:.2f} cm")
            print(f"  Maksimum Mesafe: {max_dist:.2f} cm")
            print(f"  Ortalama Mesafe: {avg_dist:.2f} cm")

            # Grafik Çizimleri
            print("\nGrafikler çizdiriliyor (matplotlib gerektirir)...")
            try:
                # 1. Mesafe Grafiği
                ornek_numaralari = [veri['ornek_no'] for veri in harita_verileri_otonom]
                mesafeler = [veri['mesafe_cm'] for veri in harita_verileri_otonom]

                plt.figure(figsize=(12, 6))
                plt.plot(ornek_numaralari, mesafeler, marker='.', linestyle='-', color='dodgerblue',
                         label='Ölçülen Mesafe')
                plt.title("Sıralı Mesafe Ölçümleri Profili")
                plt.xlabel("Örnek Numarası")
                plt.ylabel("Mesafe (cm)")
                plt.legend()
                plt.grid(True)
                plt.ylim(bottom=0)
                # plt.savefig("otonom_mesafe_profili.png")
                plt.show()

                # 2. Hız Grafiği
                if len(harita_verileri_otonom) > 1:  # Hız hesaplanabildiyse
                    hizlar = [veri['hiz_cm_s'] for veri in harita_verileri_otonom]  # İlk eleman 0 olacak şekilde

                    plt.figure(figsize=(12, 6))
                    plt.plot(ornek_numaralari, hizlar, marker='.', linestyle='-', color='crimson', label='Tahmini Hız')
                    plt.title("Tahmini Hız Profili")
                    plt.xlabel("Örnek Numarası")
                    plt.ylabel("Hız (cm/s)")
                    plt.axhline(0, color='grey', lw=0.5, linestyle='--')  # Sıfır hız çizgisi
                    plt.legend()
                    plt.grid(True)
                    # plt.savefig("otonom_hiz_profili.png")
                    plt.show()

            except ImportError:
                print("Matplotlib kütüphanesi kurulu değil veya bulunamadı. Grafikler çizilemedi.")
                print("Kurmak için: sudo pip3 install matplotlib")
            except Exception as e_plot:
                print(f"Grafik çizimi sırasında bir hata oluştu: {e_plot}")
        else:
            print("Hiç veri toplanmadı, istatistik veya grafik oluşturulamıyor.")

        print("\nPinler temizleniyor...")
        if red_led and hasattr(red_led, 'is_active') and red_led.is_active: red_led.off()
        if red_led and hasattr(red_led, 'close'): red_led.close()
        if green_led and hasattr(green_led, 'is_active') and green_led.is_active: green_led.off()
        if green_led and hasattr(green_led, 'close'): green_led.close()
        if yellow_led and hasattr(yellow_led, 'is_active') and yellow_led.is_active: yellow_led.off()
        if yellow_led and hasattr(yellow_led, 'close'): yellow_led.close()
        if sensor and hasattr(sensor, 'close'): sensor.close()

        print("Program başarıyla sonlandı.")