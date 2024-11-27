from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained CNN model
MODEL_PATH = "rgb.keras"
model = load_model(MODEL_PATH)

# Define allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(file_path):
    """
    Preprocess the image for prediction.
    Assumes the model expects images of size 126x126x3.
    """
    # Load and resize image
    img = load_img(file_path, target_size=(126, 126))  # Resize to 126x126
    img_array = img_to_array(img)  # Convert to array (126, 126, 3)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension (1, 126, 126, 3)

    # Normalize image
    img_array = img_array / 255.0  # Normalize to [0, 1]
    return img_array

@app.route("/")
def index():
    return render_template("about.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join("uploads", file.filename)

        # Save the uploaded file temporarily
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        file.save(file_path)

        try:
            # Preprocess the image and predict
            img = preprocess_image(file_path)
            prediction = model.predict(img)
            os.remove(file_path)  # Clean up uploaded file

            # Customize the prediction output based on your model
            label = "Benign" if prediction[0][0] < 0.4 else "Malignant"
            accuracy = round(float(max(prediction[0]) * 100), 2)

            return jsonify({"prediction": label, "accuracy": f"{accuracy}%"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
