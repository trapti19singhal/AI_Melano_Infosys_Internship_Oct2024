from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress TensorFlow warnings

app = Flask(__name__)
MODEL_DIR = "model/"

# List all available models in the directory
available_models = [model for model in os.listdir(MODEL_DIR) if model.endswith(".h5")]

# Helper function to load a model
def load_selected_model(model_name):
    model_path = os.path.join(MODEL_DIR, model_name)
    return load_model(model_path)

model = load_model("model/RGB_AUG.h5")
# Preprocessing helper function
def preprocess_image(image, target_size):
    image = image.resize(target_size)  # Resize the image
    image = img_to_array(image)  # Convert to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize
    return image

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html",models=available_models)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        image = Image.open(file).convert("RGB")
        processed_image = preprocess_image(image, target_size=(128, 128)) 
        prediction = model.predict(processed_image) 
        result = "Benign" if prediction[0][0] > 0.9 else "Malignant"
        confidence_percentage = round(float(prediction[0][0]) * 100)
        return jsonify({"prediction": result, "confidence": confidence_percentage})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == "__main__":
    app.run(debug=True)
