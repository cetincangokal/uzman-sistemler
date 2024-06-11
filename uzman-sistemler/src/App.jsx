import { useState } from 'react';
import axios from 'axios';

function App() {
  const [image, setImage] = useState(null);
  const [detectionStatus, setDetectionStatus] = useState(null);
  const [tumorTypes, setTumorTypes] = useState(null);
  const [resultImage, setResultImage] = useState(null);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    setImage(file);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setDetectionStatus(response.data.detection_status);
      setTumorTypes(response.data.tumor_types);
      setResultImage(`http://127.0.0.1:5000/prediction_with_boxes.jpg`);
    } catch (error) {
      console.error('Error uploading image:', error);
      setDetectionStatus("Tespit edilemedi.");
      setTumorTypes(null);
      setResultImage(null);
    }
  };

  const handleClear = () => {
    setImage(null);
    setDetectionStatus(null);
    setTumorTypes(null);
    setResultImage(null);
  };

  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-300 to-white">
      <div className="container mx-auto px-4 shadow-lg">
        <div className="min-h-[733px] max-w-[1300px] flex justify-center items-center">
          <div className="grid md:grid-cols-1 lg:grid-cols-2 gap-96">
            <div className="relative">
              <h1 className="text-3xl lg:text-4xl font-bold mb-3 text-white">
                Girdi
              </h1>
              <div className="overflow-hidden">
                {image && (
                  <img src={URL.createObjectURL(image)} alt="Uploaded" className="max-h-[250px]" />
                )}
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="px-4 py-2 mt-6 bg-gray-400 text-white rounded-lg cursor-pointer max-w-[250px]"
                />
              </div>
            </div>
            <div>
              <div className="relative">
                <h1 className="text-3xl lg:text-4xl font-bold mb-3">
                  Çıktı
                </h1>
                {resultImage && (
                  <img src={resultImage} alt="Result" className="max-h-[250px]" />
                )}
                <div className="text-xl font-semibold">Tümör Tespiti: {detectionStatus}</div>
                <div className="text-xl font-semibold">Tümör Türü: {tumorTypes}</div>
                <button
                  onClick={handleClear}
                  className="px-4 py-2 bg-red-500 text-white rounded-lg"
                >
                  Temizle
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
