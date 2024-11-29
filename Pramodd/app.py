from flask import Flask, request, render_template, redirect, url_for
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import img_to_array, load_img
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the trained model
model = load_model(r'C:\Users\91812\Downloads\archive (1) (1)\enhanced_model.h5')  # Update the path as needed

# Ensure the `uploads` folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles prediction requests."""
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
        image = load_img(file_path, target_size=(128, 128))  # Resize to match model input size

        # Convert the image to grayscale
        image = image.convert('L')  # Convert to grayscale using PIL
        image = img_to_array(image)  # Convert to numpy array

        # Ensure the shape is (128, 128, 1)
        image = np.expand_dims(image, axis=-1)  # Add channel dimension (now (128, 128, 1))
        image = np.expand_dims(image, axis=0)  # Add batch dimension (now (1, 128, 128, 1))

        # Normalize the image data
        image = image / 255.0  # Normalize pixel values to range [0, 1]

        # Make a prediction
        prediction = model.predict(image)

        # Extract the confidence and prediction result
        confidence = float(prediction[0][0])  # Confidence for "Malignant"
        result = "Malignant" if confidence > 0.5 else "Benign"
        confidence_percentage = round(confidence * 100, 2) if result == "Malignant" else round((1 - confidence) * 100, 2)

        # Render the result on the webpage
        return render_template(
            'index.html',
            uploaded_image_path=file_path,
            prediction=result,
            confidence=confidence_percentage
        )

    return "Invalid file.", 400

if __name__ == '__main__':
    app.run(debug=True)
