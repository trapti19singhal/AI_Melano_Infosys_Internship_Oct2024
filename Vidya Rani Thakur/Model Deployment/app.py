from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Load your models
models = {
    "model3": load_model(r"C:\Users\thaku\OneDrive\Desktop\Melanoma\models\model3.h5"),  # Gray Augmented Model
    "model5": load_model(r"C:\Users\thaku\OneDrive\Desktop\Melanoma\models\model5.h5")   # VGG16 Model
}

# Route to serve Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Route to serve Sample Page
@app.route('/sample')
def sample():
    return render_template('sample.html')

# Route to serve Prediction Page
@app.route('/predict', methods=['GET', 'POST'])
def predict_page():
    if request.method == 'GET':
        return render_template('predict.html')
    else:
        # Handle file upload and model selection
        if 'file' not in request.files or 'model' not in request.form:
            return jsonify({"success": False, "error": "No file or model selected"})

        file = request.files['file']
        selected_model = request.form['model']

        if selected_model not in models:
            return jsonify({"success": False, "error": "Invalid model selected"})

        # Save the file temporarily
        temp_path = "temp_image.jpg"
        file.save(temp_path)

        try:
            # Preprocess the image
            if selected_model == "model5":  # VGG16 requires RGB input
                image = Image.open(temp_path).convert("RGB")
                image = image.resize((128, 128))  # Resize to model input size
                image = np.array(image)  # Convert to numpy array
                image = preprocess_input(image)  # Apply VGG16 preprocessing
                image = np.expand_dims(image, axis=0)  # Add batch dimension
            elif selected_model == "model3":  # Gray augmented model requires grayscale input
                image = Image.open(temp_path).convert("L")
                image = image.resize((128, 128))  # Resize to model input size
                image = np.array(image) / 255.0  # Normalize pixel values
                image = np.expand_dims(image, axis=-1)  # Add channel dimension
                image = np.expand_dims(image, axis=0)  # Add batch dimension

            # Make prediction
            model = models[selected_model]
            predictions = model.predict(image)
            predicted_class = "Malignant" if predictions[0][0] > 0.5 else "Benign"
            confidence = predictions[0][0] * 100 if predicted_class == "Malignant" else (1 - predictions[0][0]) * 100

            return jsonify({
                "success": True,
                "prediction": predicted_class,
                "confidence": f"{confidence:.2f}%"
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == '__main__':
    app.run( port=5000,debug=True)
