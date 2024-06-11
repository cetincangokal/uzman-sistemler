import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image

from roboflow import Roboflow


# Roboflow API anahtarınızı kullanarak projeye erişim sağlama
rf = Roboflow(api_key='hMLv7xOrDRZbad42LO4J')
project = rf.workspace().project("beyintumoru-le2b4")
model = project.version(1).model

# Görüntü yolu
image_path = r"tumor/notumor/WhatsApp Image 2024-05-29 at 20.01.12 (1).jpeg"

# Görüntüyü yükleyin ve tahmin yapın
response = model.predict(image_path, confidence=40, overlap=30).json()

# Tahmin edilen sınıfları yazdırın
for prediction in response["predictions"]:
    class_name = prediction["class"]  # Sınıf ismi
    print(f"{class_name}")

# İşaretlenmiş görüntüyü yükleyin
image = cv2.imread(image_path)

# Tahmin edilen sonuçları görüntüye çizin
for prediction in response["predictions"]:
    x = prediction["x"]
    y = prediction["y"]
    width = prediction["width"]
    height = prediction["height"]
    confidence = prediction["confidence"]
    class_name = prediction["class"]

    # Kutucuk koordinatları
    start_point = (int(x - width / 2), int(y - height / 2))
    end_point = (int(x + width / 2), int(y + height / 2))

    # Kutucuk ve metin renkleri
    color = (0, 255, 0)  # Yeşil
    thickness = 2

    # Görüntüye kutucuk çizme
    image = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Metin koordinatları
    text = f"{class_name}: {confidence:.2f}"
    text_org = (start_point[0], start_point[1] - 10)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1

    # Görüntüye metin ekleme
    image = cv2.putText(image, text, text_org, font, font_scale, color, font_thickness, cv2.LINE_AA)

# Görüntüyü gösterme
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')  # Eksenleri gizleyin
plt.show()

# İşaretlenmiş görüntüyü kaydetme
cv2.imwrite("prediction_with_boxes.jpg", image)