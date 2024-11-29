# MelanoAI: Intelligent Skin Cancer Screening

## Overview
MelanoAI leverages advanced artificial intelligence to provide accurate and inclusive skin cancer screening. This project includes a web application that allows users to upload images of skin lesions for analysis, providing predictions and confidence levels for potential melanoma.

## Features
- **AI-Driven Analysis**: Utilizes a trained AI model to analyze skin lesion images and provide predictions.
- **User-Friendly Interface**: Easy-to-use web interface for uploading images and receiving results.
- **Educational Content**: Information on benign and malignant lesions, the ABCDEs of skin cancer, and self-check tips.
- **Responsive Design**: Accessible on various devices with a modern and clean layout.

## Project Structure
Sakthi Dharan/ 
├── app.py
├── templates/ 
│ ├── base.html
│ ├── index.html
│ ├── about.html
│ ├── info.html
│ ├── predict.html
│ ├── contact.html
│ ├── testimonials.html
│ └── blog.html
├── static/
│ ├── styles.css
│ ├── script.js
│ └── images/ 
│ ├── banner.jpg
│ ├── about.jpg
│ └── info.jpg
├── assets/ # Additional assets 
├── README.md 
├── requirements.txt 
├── Melanoai.ipynb



## Installation
1. **Clone the Repository**
    ```sh
    git clone https://github.com/trapti19singhal/AI_Melano_Infosys_Internship_Oct2024
    cd SakthiDharanMA
    ```

2. **Create a Virtual Environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the Application**
    ```sh
    python app.py
    ```

## Usage
1. **Open Your Browser**: Navigate to `http://127.0.0.1:5000/` to access the web application.
2. **Upload an Image**: Use the upload feature to select an image of a skin lesion.
3. **Get Results**: View the prediction results and confidence level provided by the AI model.

## Model and Dataset
- **Model File**: [Download from Google Drive](https://drive.google.com/file/d/15tFK7iZ6Y7ofo5hsf_71h_UoCJpYZdZg/view?usp=drive_link)
- **Dataset**: [Download from Google Drive](https://drive.google.com/file/d/19urOeOXmY-0yQnDcc29Sv871NsdHW9Pg/view?usp=drive_link)

## Model Training
If you want to retrain the model using your own dataset:
1. **Prepare Your Dataset**: Ensure your dataset is organized properly.
2. **Run the Training Notebook**: Open and run the provided Jupyter notebook for model training.
3. **Update the Model**: Replace the existing model file in `app.py` with the newly trained model.

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For inquiries or more information, please contact:
- **Name**: Sakthi Dharan M A 
- **Email**: officialsakthidharan@gmail.com
