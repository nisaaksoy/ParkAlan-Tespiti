# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:31:15 2024

@author: pc
"""

import cv2
import numpy as np

# Görüntüyü yükle
img = cv2.imread('C:/Users/pc/Downloads/otopark4.jpg')

# Görüntüyü gri tonlamaya çevirme
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gürültü azaltma (Gaussian Blur)
blurred_img = cv2.GaussianBlur(gray, (5, 5), 0)

# Kontrast artırma
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
enhanced_img = clahe.apply(blurred_img)

# Canny kenar algılama
canny_edges = cv2.Canny(enhanced_img, 100, 200)

# Sobel kenar algılama
sobelx = cv2.Sobel(enhanced_img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(enhanced_img, cv2.CV_64F, 0, 1, ksize=3)
sobel_edges = cv2.sqrt(sobelx**2 + sobely**2)

# Prewitt kenar algılama
kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

prewittx = cv2.filter2D(enhanced_img, cv2.CV_32F, kernelx)
prewitty = cv2.filter2D(enhanced_img, cv2.CV_32F, kernely)

# Prewitt kenarları karekök alınarak birleştiriliyor
prewitt_edges = cv2.sqrt(prewittx**2 + prewitty**2)

# Kenarları bul ve konturları çıkar (Canny kenar algılamayı kullanıyoruz)
contours, _ = cv2.findContours(canny_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Park yerlerini belirlemek için dikdörtgen segmentler çiz
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    
    # Kenarların belirli bir boyutun üzerinde olup olmadığını kontrol et (minimum boyut ayarı)
    if w > 50 and h > 50:
        # Dikdörtgen çiz (yeşil: park alanı)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Boş mu dolu mu kontrolü: Segment içinde yeterli kenar varsa dolu, yoksa boş
        park_area = canny_edges[y:y+h, x:x+w]
        non_zero_pixels = cv2.countNonZero(park_area)
        
        # Kenar yoğunluğu eşiği belirlenir (non-zero pixel sayısı)
        if non_zero_pixels > 1000:  # Doluluk tespiti için bir eşik değeri
            cv2.putText(img, "DOLU", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(img, "BOS", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Kenar algılama sonuçlarını göster
cv2.imshow('Canny Kenar Algılama', canny_edges)
cv2.imshow('Sobel Kenar Algılama', sobel_edges)
cv2.imshow('Prewitt Kenar Algılama', prewitt_edges)
cv2.imshow('Park Yeri Tespiti', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

