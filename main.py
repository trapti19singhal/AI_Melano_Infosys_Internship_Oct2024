from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, flash, send_from_directory
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

model = load_model("./vgg16_model6.h5")

@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        img = Image.open(file).convert("RGB").resize((64, 64))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)
        class_names = ["Benign", "Malignant"]
        predicted_class = class_names[int(prediction[0] > 0.5)]
        confidence = round(float(prediction[0]) * 100, 2)
        if predicted_class == "Benign":
            confidence = 100 - confidence

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence,
            'image_url': f'/{file_path}'
        })
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)