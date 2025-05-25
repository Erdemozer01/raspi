import cv2
import numpy as np
import requests

# Telefonunuzdaki IP Webcam uygulamasının sağladığı IP adresi ve port numarasını buraya girin

url = "http://192.168.1.3:8080/"

while True:

    try:

        img_resp = requests.get(url)

        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)

        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if img is not None:

            image = cv2.resize(img, (640, 480))  # Görüntü boyutunu ayarlayabilirsiniz

            cv2.putText(image, 'Telefon Kamerası', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Telefon Kamerası - IP Webcam", image)

        else:

            print("Görüntü alınamadı.")

    except requests.exceptions.RequestException as e:

        print(f"Bağlantı hatası: {e}")

    except Exception as e:

        print(f"Bir hata oluştu: {e}")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()