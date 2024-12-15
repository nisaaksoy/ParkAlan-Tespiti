# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 12:52:22 2024

@author: pc
"""

import cv2
import pickle

# Noktaları dosyadan yükle
try:
    with open("n", "rb") as f:
        liste = pickle.load(f)
except FileNotFoundError:
    liste = []

# Resmi yükle ve boyutları al
img = cv2.imread("C:\\Users\\pc\\.spyder-py3\\otopark\\otopark.png")
if img is None:
    print("Resim yüklenemedi!")
    exit()
img_height, img_width = img.shape[:2]  # Resim boyutlarını al

# Mouse olaylarını işleyen fonksiyon
def mouse(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:  # Sol tık ile nokta ekleme
        liste.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:  # Sağ tık ile nokta silme
        for i, pos in enumerate(liste):
            x1, y1 = pos
            if x1 < x < x1 + 60 and y1 < y < y1 + 15:  # Güncellenen boyutlar (60, 15)
                liste.pop(i)
                break  # Nokta silindikten sonra döngüyü durdur
    # Noktalar listesini dosyaya yaz
    with open("n", "wb") as f:
        pickle.dump(liste, f)

# Görüntüyü işleme ve gösterme
while True:
    img_copy = img.copy()  # Orijinal resmi bozmamak için kopyasını kullan
    for l in liste:
        cv2.rectangle(img_copy, (l[0], l[1]), (l[0] + 60, l[1] + 15), (255, 0, 0), 2)  # Boyut güncellendi

    # Görüntüyü göster
    cv2.imshow("Oto Resim", img_copy)
    cv2.setMouseCallback("Oto Resim", mouse)

    # 'q' tuşuna basılırsa döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Pencereleri kapat
cv2.destroyAllWindows()
