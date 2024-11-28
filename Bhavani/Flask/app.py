from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Load the pre-trained model
model = load_model(r'E:\Saved_model\Melanoma_detection_model.keras')

# Define the target size (as used during training)
target_size = (128, 128)

# Route to home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Open the image file
        img = Image.open(file)
        img = img.resize(target_size)  # Resize the image to 64x64
        img = np.array(img)  # Convert image to numpy array

        if img.shape[-1] == 4:  # If the image has an alpha channel (RGBA), discard it
            img = img[..., :3]

        # Normalize the image (as was done during training)
        img = img / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)

        # Predict the class
        prediction = model.predict(img)
        class_label = 'Malignant' if prediction[0][0] > 0.5 else 'Benign'

        # Normalize confidence based on class label
        confidence = (
            prediction[0][0] * 100 if class_label == 'Malignant' else (1 - prediction[0][0]) * 100
        )

        return jsonify({
            "class": class_label,
            "confidence": f"{confidence:.2f}%"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
