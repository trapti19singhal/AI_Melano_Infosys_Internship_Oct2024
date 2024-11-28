import os
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf

# Initialize Flask app
app = Flask(__name__)

# Define the allowed extensions for image files
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the pre-trained model
model = tf.keras.models.load_model(r'C:\Users\HP\Downloads\melanoma_cancer_dataset_without_duplicates\models\vgg-16.keras')

# Set the upload folder within the static directory
app.config['uploads'] = os.path.join(
    r'C:\Users\HP\Downloads\melanoma_cancer_dataset_without_duplicates', 'Website', 'static', 'uploads'
)

# Ensure the upload folder exists
os.makedirs(app.config['uploads'], exist_ok=True)

# Function to preprocess the image and predict
def predict_image(image_path):
    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize((150, 150))  # Resize image to match model input size
    img = tf.keras.preprocessing.image.img_to_array(img)  # Convert to NumPy array
    img = tf.expand_dims(img, axis=0)  # Add batch dimension
    img = img / 255.0  # Normalize to [0, 1]
    
    # Make the prediction
    prediction = model.predict(img)
    
    # Class names
    class_names = ['The image is classified as Benign', 'The image is classified as Malignant']
    predicted_class = class_names[int(prediction[0] > 0.5)]  # Binary classification
    
    # Extract scalar prediction score
    return predicted_class, float(prediction[0][0])  # Convert prediction score to scalar

# Prediction page route
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']

        # Check if the file is valid
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)

            # Define the full file path for saving the uploaded image
            img_path = os.path.join(app.config['uploads'], filename)

            # Save the uploaded image
            file.save(img_path)

            # Make the prediction
            result, prediction_score = predict_image(img_path)

            # Generate the URL for the uploaded image
            img_url = url_for('static', filename=f'uploads/{filename}')

            # Prepare message based on prediction
            if "Malignant" in result:
                warning_message = "Warning: The image suggests a Malignant condition. Please consult a healthcare provider."
            else:
                warning_message = "The image suggests a Benign condition. No immediate action needed."

            # Render the result with warning message
            return render_template(
                'prediction.html',
                title="Prediction",
                result=result,
                warning_message=warning_message,
                img_url=img_url,
                accuracy=f"{prediction_score * 100:.2f}%"  # Use scalar value for formatting
            )

    return render_template('prediction.html', title="Prediction")

# Homepage route
@app.route('/')
def index():
    return render_template('index.html', title="Home")

# Description page route
@app.route('/description')
def description():
    return render_template('description.html', title="Description")

# Contact Us page route
@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
