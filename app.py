from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import numpy as np
import joblib
import pandas as pd
import json
import sys
from pathlib import Path

# First try to use tensorflow.keras (preferred)
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    print("✓ Successfully imported TensorFlow Keras")
    keras_available = True
    keras_source = "tensorflow"
except ImportError:
    # Fallback to standalone Keras
    try:
        import keras
        from keras.models import load_model
        from keras.preprocessing import image
        print("✓ Successfully imported standalone Keras")
        keras_available = True
        keras_source = "standalone"
    except ImportError:
        print("✗ Could not import Keras - image model functionality will be limited")
        keras_available = False
        keras_source = None
        # Create placeholder functions
        def load_model(path):
            print(f"Would load model from {path}, but Keras is not available")
            return None
            
        class DummyImage:
            @staticmethod
            def load_img(*args, **kwargs):
                return None
                
            @staticmethod
            def img_to_array(*args, **kwargs):
                return np.zeros((224, 224, 3))
                
        image = DummyImage()

# Get base directory for the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Parent directory of SkinDiseaseAssistant

# Initialize Flask app with correct template and static folders
app = Flask(__name__, 
            template_folder=os.path.join(PROJECT_ROOT, 'templates'),
            static_folder=os.path.join(PROJECT_ROOT, 'static'))

print(f"Template folder: {os.path.join(PROJECT_ROOT, 'templates')}")
print(f"Static folder: {os.path.join(PROJECT_ROOT, 'static')}")

# Try to identify the correct model file
def find_model_file(base_name, extensions=['.keras', '.h5', '.model'], search_dir=BASE_DIR):
    """Try to find the model file with different extensions"""
    for ext in extensions:
        path = os.path.join(search_dir, base_name + ext)
        if os.path.exists(path):
            print(f"Found model file: {path}")
            return path
    
    # If no exact match, try to find any model file in the directory
    for file in os.listdir(search_dir):
        if file.endswith(tuple(extensions)):
            full_path = os.path.join(search_dir, file)
            print(f"Found alternative model file: {full_path}")
            return full_path
            
    return None

# Load models and data
try:
    # Load the trained CNN model
    model_path = find_model_file('skin_disease_model')
    if model_path and keras_available:
        try:
            img_model = load_model(model_path)
            print(f"✅ Image model loaded successfully from {model_path}")
        except Exception as e:
            print(f"❌ Error loading image model: {e}")
            img_model = None
    else:
        print(f"❌ Image model file not found or Keras not available")
        img_model = None
    
    # Load the text-based model
    text_model_path = os.path.join(BASE_DIR, '..', 'skin-quiz-backend', 'text_model.pkl')
    if os.path.exists(text_model_path):
        text_model, label_encoders, target_encoder = joblib.load(text_model_path)
        print(f"✅ Text model loaded successfully from {text_model_path}")
    else:
        print(f"❌ Text model file not found at {text_model_path}, trying alternative paths")
        
        # Try alternative path
        alt_text_model_path = os.path.join(os.path.dirname(BASE_DIR), 'skin-quiz-backend', 'text_model.pkl')
        if os.path.exists(alt_text_model_path):
            text_model, label_encoders, target_encoder = joblib.load(alt_text_model_path)
            print(f"✅ Text model loaded successfully from {alt_text_model_path}")
        else:
            print(f"❌ Text model file not found at alternative path either")
            text_model = None
            label_encoders = {}
            target_encoder = None
    
    # Load recommendations
    rec_path = os.path.join(BASE_DIR, 'recommendations.json')
    if os.path.exists(rec_path):
        with open(rec_path, 'r') as f:
            recommendations = json.load(f)
        print(f"✅ Recommendations loaded successfully from {rec_path}")
    else:
        # Try alternative path in skin-quiz-backend
        alt_rec_path = os.path.join(os.path.dirname(BASE_DIR), 'skin-quiz-backend', 'recommendations.json')
        if os.path.exists(alt_rec_path):
            with open(alt_rec_path, 'r') as f:
                recommendations = json.load(f)
            print(f"✅ Recommendations loaded successfully from alternative path {alt_rec_path}")
        else:
            print(f"❌ Recommendations file not found in either path")
            recommendations = {}
        
    models_loaded = (img_model is not None) or (text_model is not None)
    print(f"Models loaded status: {models_loaded}")
    
except Exception as e:
    models_loaded = False
    print(f"❌ Error loading models: {e}")
    print("Starting Flask app with limited functionality")

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to preprocess the image for the CNN model
def preprocess_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalize the image
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

# Function to predict the disease from image
def predict_disease_from_image(img_path):
    if img_model is None:
        return "Model Not Loaded", 0
        
    img_array = preprocess_image(img_path)
    if img_array is None:
        return "Image Processing Error", 0
        
    predictions = img_model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    confidence = np.max(predictions) * 100
    
    # Get class labels - hardcoded for now based on your dataset
    class_labels = ['acne', 'eksim', 'herpes', 'panu', 'rosacea']
    
    return class_labels[predicted_class[0]], confidence

# Function to predict disease from questionnaire answers
def predict_disease_from_text(user_data):
    if text_model is None:
        return "Model Not Loaded", 0
        
    try:
        # Convert to DataFrame
        df = pd.DataFrame([user_data])
        
        # Encode using label encoders
        for column in df.columns:
            if column in label_encoders:
                df[column] = label_encoders[column].transform(df[column])
        
        # Predict disease
        prediction = text_model.predict(df)
        predicted_disease = target_encoder.inverse_transform(prediction)[0]
        
        # Normalize disease name to match recommendations.json keys
        predicted_disease = normalize_disease_name(predicted_disease)
        
        # Get confidence score
        probabilities = text_model.predict_proba(df)[0]
        confidence = max(probabilities) * 100
        
        return predicted_disease, confidence
    except Exception as e:
        print(f"Error predicting from text: {e}")
        return "Prediction Error", 0

# Function to normalize disease names to match recommendations.json keys
def normalize_disease_name(disease_name):
    # Convert to lowercase and remove extra spaces
    disease_name = disease_name.lower().strip()
    
    # Map common variations to standard names in recommendations.json
    disease_mapping = {
        'acne vulgaris': 'acne',
        'acne': 'acne',
        'eczema': 'eksim',
        'eksim': 'eksim',
        'dermatitis': 'eksim',
        'atopic dermatitis': 'eksim',
        'herpes simplex': 'herpes',
        'herpes': 'herpes',
        'cold sore': 'herpes',
        'tinea versicolor': 'panu',
        'panu': 'panu',
        'rosacea': 'rosacea',
        'facial redness': 'rosacea'
    }
    
    # Return the mapped standard name if available, otherwise return the original
    return disease_mapping.get(disease_name, disease_name)

# Function to get recommendations for a disease
def get_recommendations(disease):
    if disease in recommendations:
        return recommendations[disease]
    else:
        return {
            "description": "No detailed description available for this condition.",
            "products": [{"name": "Gentle Cleanser", "description": "A mild, non-irritating cleanser is recommended for all skin conditions."}],
            "diet": [{"name": "Stay Hydrated", "description": "Drinking plenty of water helps maintain skin health regardless of condition."}]
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict-image', methods=['POST'])
def predict_image():
    if not models_loaded:
        return jsonify({"error": "Models are not loaded properly"}), 500
        
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        upload_folder = os.path.join(BASE_DIR, 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Predict the disease
        disease, confidence = predict_disease_from_image(file_path)

        # Get recommendations
        recommendation = get_recommendations(disease)

        # Return the result
        return jsonify({
            "disease": disease,
            "description": recommendation["description"],
            "confidence_score": f"{confidence:.2f}%",
            "product_recommendations": recommendation["products"],
            "diet_recommendations": recommendation["diet"],
            "image_path": file_path
        })

    return jsonify({"error": "Invalid file type"}), 400

@app.route('/predict-quiz', methods=['POST'])
def predict_quiz():
    if not models_loaded:
        return jsonify({"error": "Models are not loaded properly"}), 500
        
    try:
        # Get form data
        user_data = {
            'Age Group': request.form.get('age_group'),
            'Skin Type': request.form.get('skin_type'),
            'Main Issue': request.form.get('main_issue'),
            'Duration': request.form.get('duration'),
            'Past Condition': request.form.get('past_condition'),
            'Using Products': request.form.get('using_products'),
            'Allergies': request.form.get('allergies'),
            'Sun Exposure': request.form.get('sun_exposure'),
            'Exercise': request.form.get('exercise'),
            'Sweat': request.form.get('sweat')
        }
        
        # Validate form data
        for key, value in user_data.items():
            if not value:
                return jsonify({"error": f"Missing field: {key}"}), 400
        
        # Predict disease
        disease, confidence = predict_disease_from_text(user_data)
        
        # Get recommendations
        recommendation = get_recommendations(disease)
        
        # Return the result
        return jsonify({
            "disease": disease,
            "description": recommendation["description"],
            "confidence_score": f"{confidence:.2f}%",
            "product_recommendations": recommendation["products"],
            "diet_recommendations": recommendation["diet"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/result')
def result():
    return render_template('result.html')

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)