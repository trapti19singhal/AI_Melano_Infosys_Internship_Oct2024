import csv
import os
from flask import Flask, request, render_template, jsonify
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import numpy as np

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_evaluation_results():
    results = {}
    with open('static\evaluation_results.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            results[row['Model']] = {
                'Loss': row['Loss'],
                'Accuracy': row['Accuracy']
            }
    return results
# Route to serve the upload form (GET method)
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Route to handle the file upload and prediction (POST method)
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    model_name = request.form.get('model')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the image temporarily
        filename = secure_filename(file.filename)
        img_path = os.path.join('uploads', filename)
        
        # Ensure uploads folder exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        # Save the uploaded file
        file.save(img_path)

        # Preprocess the image for prediction
        if 'Normalize_Gray' in model_name or 'Augmented_Normalize_Gray' in model_name:
            img = image.load_img(img_path, target_size=(224, 224), color_mode='grayscale')
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = img_array.reshape((1, 224, 224, 1))
        else:
            img = image.load_img(img_path, target_size=(224, 224), color_mode='rgb')
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = img_array.reshape((1, 224, 224, 3))

        # Load the selected model
        model_path = os.path.join('static/models', f'{model_name}.keras')
        model = load_model(model_path)

        # Make the prediction
        prediction = model.predict(img_array)
        predicted_class = (prediction > 0.5).astype("int32")

        # Return the prediction result and accuracy as a JSON response
        return jsonify({
            'prediction': int(predicted_class[0][0]),
            'probability': float(prediction[0][0])
        })

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/details')
def detail():
    evaluation_results = get_evaluation_results()
    return render_template('details.html', evaluation_results=evaluation_results)

@app.route('/advance', methods=['GET', 'POST'])
def advance_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the image temporarily
        filename = secure_filename(file.filename)
        img_path = os.path.join('uploads', filename)
        
        # Ensure uploads folder exists
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        
        # Save the uploaded file
        file.save(img_path)

        # Preprocess the image for prediction
        img = image.load_img(img_path, target_size=(224, 224), color_mode='rgb')
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = img_array.reshape((1, 224, 224, 3))

        # List all models in the static directory
        model_dir = 'static'
        model_files = [f for f in os.listdir(model_dir) if f.endswith('.keras')]
        
        predictions = {}
        
        for model_file in model_files:
            model_path = os.path.join(model_dir, model_file)
            model = load_model(model_path)
            
            # Make the prediction
            prediction = model.predict(img_array)
            predicted_class = (prediction > 0.5).astype("int32")
            
            # Store the prediction result and accuracy
            predictions[model_file] = {
                'prediction': int(predicted_class[0][0]),
                'probability': float(prediction[0][0])
            }

        # Return the predictions for all models as a JSON response
        return jsonify(predictions)

    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
