from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

# Load the pre-trained CNN model
MODEL_PATH = r"C:\Users\shravyacheekoti\Desktop\Infosys cancer project\model5.keras"
model = load_model(MODEL_PATH)

# Ensure the uploads folder exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(img_path):
    # Preprocess the image for the CNN model
    img = image.load_img(img_path, target_size=(128, 128))  # Resize to model input
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    prediction = model.predict(img_array)
    predicted_class = "Malignant" if prediction[0][0] > 0.5 else "Benign"
    confidence = prediction[0][0] if predicted_class == "Malignant" else 1 - prediction[0][0]
    return predicted_class, confidence

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    predicted_class = None
    confidence = None
    image_path = None

    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            flash('No file uploaded!')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Save and process the file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Get the prediction result and confidence
            predicted_class, confidence = predict_image(file_path)

            # Make the image path relative for proper URL rendering
            image_path = os.path.join('uploads', file.filename)  # Use relative path for display in the HTML

    return render_template('predict.html', predicted_class=predicted_class, image_path=image_path, confidence=confidence)

if __name__ == '__main__':
    app.run(port=3000, debug=True)