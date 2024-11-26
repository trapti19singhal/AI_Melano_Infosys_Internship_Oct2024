from flask import Flask,render_template,request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

# loading the model
model = load_model('vgg16_model.keras')

app = Flask(__name__)


@app.route("/",methods=['GET']) 
def home():
    return render_template('about.html') 

@app.route("/samples",methods=['GET'])
def samples():
    benign_images = []
    malignant_images = []

    benign_dir = os.path.join('static','images','benign')
    malignant_dir = os.path.join('static','images','malignant')

    for filename in os.listdir(benign_dir):
        if filename.endswith(('.png','.jpg','.jpeg')):
            benign_images.append({'url':os.path.join(benign_dir,filename)})

    for filename in os.listdir(malignant_dir):
        if filename.endswith(('.png','.jpg','.jpeg')):
            malignant_images.append({'url':os.path.join(malignant_dir,filename)})

    return render_template('sample.html',benign_images=benign_images,malignant_images=malignant_images)  

@app.route("/predict",methods=['POST',"GET"])
def predict():
    if request.method == 'POST':
        imagefile = request.files['imagefile']
        # Save the image file to images folder
        image_path = os.path.join('static', 'images', imagefile.filename)
        imagefile.save(image_path)
        # Preprocessing the image 
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        # Predicting the image
        prediction = model.predict(img_array)
        print(prediction)
        classnames = ['Benign', 'Malignant']
        result = classnames[np.argmax(prediction)]
        accuracy = np.max(prediction) * 100
        accuracy = round(accuracy, 2)
        return render_template('predict.html', prediction=result, accuracy=accuracy, file_path=image_path)
    else:
        return render_template('predict.html')
    
    

@app.route("/about",methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/contact",methods=['GET'])
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(port=3003,debug=True)