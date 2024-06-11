from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
from roboflow import Roboflow
import os

app = Flask(__name__)
CORS(app)  # CORS'u etkinleştirin

# Roboflow API anahtarınızı kullanarak projeye erişim sağlama
rf = Roboflow(api_key='hMLv7xOrDRZbad42LO4J')
project = rf.workspace().project("beyintumoru-le2b4")
model = project.version(1).model

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    image_path = 'uploaded_image.jpg'
    file.save(image_path)

    # Görüntüyü yükleyin ve tahmin yapın
    response = model.predict(image_path, confidence=40, overlap=30).json()

    # Tahmin edilen sınıfları ve tespit durumunu yazdırın
    tumor_types = []
    detection_status = "Tespit edilmedi"
    for prediction in response["predictions"]:
        class_name = prediction["class"]
        tumor_types.append(class_name)
        detection_status = "Tespit edildi"

    if tumor_types:
        tumor_types_str = ", ".join(tumor_types)
    else:
        tumor_types_str = "Tümör tespit edilmedi"

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

    # İşaretlenmiş görüntüyü kaydetme
    result_image_path = "prediction_with_boxes.jpg"
    cv2.imwrite(result_image_path, image)

    return jsonify({
        'detection_status': detection_status,
        'tumor_types': tumor_types_str,
        'result_image': result_image_path
    })

@app.route('/prediction_with_boxes.jpg')
def get_result_image():
    return send_from_directory(os.getcwd(), 'prediction_with_boxes.jpg')

if __name__ == '__main__':
    app.run(debug=True)
