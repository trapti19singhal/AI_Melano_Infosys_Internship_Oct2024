from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load your trained model
model = load_model(r"D:\Infosys Internship\App\rgbaug.h5")

def preprocess_image(img):
    img = img.resize((300, 300))  # Ensure this matches your model's expected input shape
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize
    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return render_template('predict.html', result=None, error_message="No file uploaded. Please upload an image.")

        try:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            img = Image.open(file_path)
            processed_image = preprocess_image(img)
            prediction = model.predict(processed_image)
            result_label = 'Positive (Malignant)' if prediction[0][0] > 0.5 else 'Negative (Benign)'
            confidence = round(float(prediction[0][0]) * 100, 2)

            result = {
                'label': result_label,
                'confidence': confidence
            }
            uploaded_image_url = url_for('static', filename=f'uploads/{filename}')
            return render_template('predict.html', result=result, uploaded_image_url=uploaded_image_url, error_message=None)
        except Exception as e:
            return render_template('predict.html', result=None, error_message=str(e))
    return render_template('predict.html', result=None)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Process the form data or send an email
        return render_template('contact.html', success=True)
    return render_template('contact.html', success=False)

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)
