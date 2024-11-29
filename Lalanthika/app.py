from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
from keras.preprocessing import image
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Define the allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Path for uploading images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the pre-trained model
model = tf.keras.models.load_model('model/model4.h5')

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(img_path):
    # Load and preprocess the image
    img = image.load_img(img_path, target_size=(128, 128))  # Resize to match model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize image (assuming model was trained with normalized images)

    # Get prediction probabilities
    prediction = model.predict(img_array)
    
    # Extract the confidence score and predicted class
    confidence_score = prediction[0][0] * 100  # Convert to percentage
    predicted_class = "Malignant" if prediction[0][0] > 0.5 else "Benign"
    predicted_class_num = 1 if prediction[0][0] > 0.5 else 0  # Return 1 for Malignant, 0 for Benign

    # Return the class, numeric class, and confidence score
    return predicted_class, predicted_class_num, round(confidence_score, 2)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Ensure the filename is secure
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Call the predict_image function to get the prediction, class, and confidence
            predicted_class, predicted_class_num, confidence_score = predict_image(filepath)

            # Pass the filename, prediction, class, and confidence score to the result page
            return render_template('result.html', filename=filename, 
                                   prediction=predicted_class, 
                                   class_num=predicted_class_num,
                                   confidence=confidence_score)

    return render_template('index.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
