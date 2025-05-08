import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Define dataset paths
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "train")
print(f"Using dataset path: {base_dir}")

# Make sure the path exists
if not os.path.exists(base_dir):
    raise FileNotFoundError(f"Dataset directory not found: {base_dir}. Please verify the path.")

# Image size and batch size
img_size = (224, 224)
batch_size = 32

# Load the dataset
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)  # Splitting dataset for validation

train_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",  # Multi-class classification
    subset="training"
)

val_generator = train_datagen.flow_from_directory(
    base_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical",
    subset="validation"
)

# Get class labels
class_labels = list(train_generator.class_indices.keys())
print("Class Labels:", class_labels)

# Define CNN Model
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(224, 224, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dense(len(class_labels), activation="softmax")  # Multi-class output
])

# Compile Model
model.compile(optimizer="adam",
              loss="categorical_crossentropy",  # Correct loss function for multi-class classification
              metrics=["accuracy"])

# Train Model
model.fit(train_generator, validation_data=val_generator, epochs=10)

# Save Model
model.save("skin_disease_model.keras")
print("✅ Model Saved Successfully!")


# Function to predict test images
def predict_skin_condition(model_path, img_path):
    model = load_model(model_path)

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Reshape for model input

    prediction = model.predict(img_array)
    predicted_class = class_labels[np.argmax(prediction)]  # Get the highest confidence class

    print(f"✅ Predicted Skin Condition: {predicted_class}")

# Example usage: Replace with your test image path
test_image_path = "/content/test_image2.jpg"  # Change this to your test image path
predict_skin_condition("skin_disease_model.keras", test_image_path)
