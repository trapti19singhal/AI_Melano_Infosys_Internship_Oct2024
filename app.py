from flask import Flask, render_template, request, jsonify
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import os
import io
import uuid

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

app = Flask(__name__)

# Create uploads folder if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

# Load the trained model
model = load_model("Augmented_Grayscale_Model.h5")  # Replace with your actual model path
print("Model loaded successfully!")

# Helper function for preprocessing images
def preprocess_image(image, target_size):
    """
    Resize and preprocess the image for model input.
    """
    image = image.resize(target_size)  # Resize the image to match model input size
    image = img_to_array(image)  # Convert image to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Normalize pixel values
    return image

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  

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
        image_path = os.path.join("static/uploads", unique_filename)

        # Save the image to the "static/uploads" folder
        file.save(image_path)

        image = Image.open(image_path).convert("RGB")  
        processed_image = preprocess_image(image, target_size=(150, 150))  

        # Predict using the model
        prediction = model.predict(processed_image)
        confidence = float(prediction[0][0])  # Confidence score
        result = "Malignant" if confidence > 0.5 else "Benign"
        confidence_percentage = round(confidence * 100, 2) if result == "Malignant" else round((1 - confidence) * 100, 2)

        # Return the prediction result and image path to the template
        return render_template("index.html", prediction=result,confidence=confidence_percentage,image_path=image_path)
  
    except Exception as e:
        return jsonify({"error": f"Error processing image: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
