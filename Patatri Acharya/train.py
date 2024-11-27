'''from flask import Flask, render_template, request

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import ResNet50

app = Flask(__name__)
model = VGG16()

@app.route('/', methods=['GET'])
def hello_word():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imagefile= request.files['imagefile']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]

    classification = '%s (%.2f%%)' % (label[1], label[2]*100)


    return render_template('index.html', prediction=classification)


if __name__ == '__main__':
    app.run(port=3000, debug=True)'''

from flask import Flask, request, render_template, jsonify, redirect, url_for
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)

# Load the trained ML model
MODEL_PATH = r"C:\Users\KIIT\Downloads\melanoma_model\melanoma_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Define a function for preprocessing
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224), color_mode='grayscale')
    img_array = img_to_array(img)  # Shape: (224, 224, 1)

    # Convert grayscale to RGB by repeating the grayscale channel three times
    img_array = np.repeat(img_array, 3, axis=-1)  # Shape: (224, 224, 3)

    # Normalize the image
    img_array = img_array / 255.0  # Normalize pixel values to [0, 1]

    # Add a batch dimension
    img_array = np.expand_dims(img_array, axis=0)  # Shape: (1, 224, 224, 3)

    return img_array

# Define the home route
@app.route("/")
def home():
    return render_template("index.html")  # Ensure index.html is in the templates folder

# Route to handle predictions
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the file temporarily
    file_path = os.path.join(r"C:\Users\KIIT\Desktop\PizzaAppChatbot\images", file.filename)
    os.makedirs(r"C:\Users\KIIT\Desktop\PizzaAppChatbot\images", exist_ok=True)
    file.save(file_path)
        
    img_array = preprocess_image(file_path)
    prediction = model.predict(img_array)[0][0]  # Model output
    confidence = round(float(prediction) * 100, 1) if prediction > 0.5 else round((1 - float(prediction)) * 100, 2)
    result = "Malignant" if prediction > 0.5 else "Benign"
        
    return render_template("index.html", confidence=f"{confidence}%", result=result)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
