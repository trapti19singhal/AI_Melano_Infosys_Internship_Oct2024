from flask import Flask, render_template, request, jsonify
import numpy as np
import sys
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import os
import uuid

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Flask application
app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained model
try:
    model = load_model("RGB_Augmented_Model.h5")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)  # Exit if the model cannot be loaded

# Helper function for image preprocessing
def preprocess_image(image, target_size):
    """
    Resize and preprocess the image for model input.
    """
    try:
        image = image.resize(target_size)  # Resize to target size
        image = img_to_array(image)  # Convert to numpy array
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        image = image / 255.0  # Normalize pixel values
        return image
    except Exception as e:
        print(f"Error in preprocessing image: {e}")
        raise

# Flask routes
@app.route("/", methods=["GET"])
def home():
    return render_template("frontend.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "imagefile" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["imagefile"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Generate a unique filename for the uploaded image
        unique_filename = str(uuid.uuid4()) + ".jpg"
        image_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Save the file to the uploads folder
        file.save(image_path)

        # Preprocess the image
        image = Image.open(image_path).convert("RGB")
        processed_image = preprocess_image(image, target_size=(150, 150))

        # Perform prediction
        prediction = model.predict(processed_image)
        confidence = float(prediction[0][0])
        result = "Malignant" if confidence > 0.5 else "Benign"
        confidence_percentage = round(confidence * 100, 2) if result == "Malignant" else round((1 - confidence) * 100, 2)

        return render_template("frontend.html", 
                               prediction=result, 
                               confidence=confidence_percentage, 
                               image_path=image_path)
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
