import os
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import gdown

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_model(model_name):
    model_drive_links = {
        "final_Unique_Augmented_Normalize_Gray_Model": "1fmIEqNssmqJ-Nhg6lbQrrtM1of79lCGV",
        "final_Unique_RGB_Model": "1fRwRbIJjXGxfZTl8Ahsz9yIVDxEHYq9B",
        "final_Unique_Normalize_Gray_Model": "1flSMq2QITIwWsFMRhfJaTQwGeM4DvRQv",
        "final_Unique_Augmented_RGB_Model": "1flrTQ3521SEy_jjwVcFKHrtn2ftkTxPh"
    }
    model_path = os.path.join('models', f'{model_name}.keras')
    if not os.path.exists('models'):
        os.makedirs('models')
    if not os.path.exists(model_path):
        if model_name in model_drive_links:
            gdown.download(f"https://drive.google.com/uc?id={model_drive_links[model_name]}", model_path, quiet=False)
        else:
            raise ValueError("Model name not found in the predefined Google Drive links.")
    return model_path

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    model_name = request.form.get('model')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img_path = os.path.join('uploads', filename)
        
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        file.save(img_path)

        model_path = download_model(model_name)
        model = load_model(model_path)

        if 'Normalize_Gray' in model_name or 'Augmented_Normalize_Gray' in model_name:
            img = image.load_img(img_path, target_size=(224, 224), color_mode='grayscale')
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = img_array.reshape((1, 224, 224, 1))
        else:
            img = image.load_img(img_path, target_size=(224, 224), color_mode='rgb')
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = img_array.reshape((1, 224, 224, 3))

        prediction = model.predict(img_array)
        predicted_class = (prediction > 0.5).astype("int32")

        return jsonify({
            'prediction': int(predicted_class[0][0]),
            'probability': float(prediction[0][0])
        })

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/details')
def detail():
    return render_template('details.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)