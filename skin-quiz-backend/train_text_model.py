# train_text_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
df = pd.read_csv('skin_quiz_data.csv')

# Separate features and target
X = df.drop('Disease', axis=1)  # Features (quiz answers)
y = df['Disease']               # Target (disease)

# Encode text answers to numbers
label_encoders = {}
for column in X.columns:
    le = LabelEncoder()
    X[column] = le.fit_transform(X[column])
    label_encoders[column] = le

# Encode the target (Disease) also
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model and encoders
with open('text_model.pkl', 'wb') as f:
    pickle.dump((model, label_encoders, target_encoder), f)

print(" Model trained and saved successfully!")
