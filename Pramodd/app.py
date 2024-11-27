from flask import Flask, request, render_template, redirect, url_for
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array, load_img
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the trained model
model = load_model('enhanced_model.h5')

# Ensure the `uploads` folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part in the request.", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected.", 400

    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Preprocess the image
        image = load_img(file_path, target_size=(128, 128))  # Resize to (128, 128)
        
        # Convert the image to grayscale
        image = image.convert('L')  # Convert to grayscale using PIL
        image = img_to_array(image)  # Convert to numpy array

        # Ensure the shape is (128, 128, 1)
        image = np.expand_dims(image, axis=-1)  # Add channel dimension (now (128, 128, 1))
        image = np.expand_dims(image, axis=0)  # Add batch dimension (now (1, 128, 128, 1))

        # Make a prediction
        prediction = model.predict(image)

        # Convert prediction to a human-readable label
        result = "Malignant" if prediction[0][0] > 0.5 else "Benign"
        accuracy = round(float(prediction[0][0]) * 100, 2) if result == "Malignant" else round(float(1 - prediction[0][0]) * 100, 2)

        return render_template(
            'index.html',
            uploaded_image_path=file_path,
            prediction=result,
            accuracy=accuracy
        )

    return "Invalid file.", 400

if __name__ == '__main__':
    app.run(debug=True)
