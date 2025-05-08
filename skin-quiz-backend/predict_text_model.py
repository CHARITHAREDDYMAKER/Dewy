import joblib
import pandas as pd
import json
import os

# Load model and encoders
model, label_encoders, target_encoder = joblib.load('text_model.pkl')

# Load recommendations
current_dir = os.path.dirname(os.path.abspath(__file__))
rec_path = os.path.join(current_dir, 'recommendations.json')
if os.path.exists(rec_path):
    with open(rec_path, 'r') as f:
        recommendations = json.load(f)
    print(f"Recommendations loaded successfully from {rec_path}")
else:
    print(f"Recommendations file not found at {rec_path}")
    recommendations = {}

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

# Function to ask user questions safely with option numbers
def ask_question(prompt, options):
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    while True:
        try:
            choice = int(input("Enter choice number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("❌ Invalid number. Try again.")
        except:
            print("❌ Please enter a valid number.")

# Get user inputs
user_data = {}
user_data['Age Group'] = ask_question("What is your age group?", [
    'Under 13', '13–18', '19–30', '31–45', '46–60', 'Over 60'])

user_data['Skin Type'] = ask_question("What is your skin type?", [
    'Oily', 'Dry', 'Combination', 'Normal', 'Sensitive', 'Not sure'])

user_data['Main Issue'] = ask_question("What is the main issue you're experiencing?", [
    'Acne / Pimples', 'Redness / Rashes', 'Dry or Flaky Skin',
    'Dark spots or Hyperpigmentation', 'Itching or Irritation', 'Other / Not sure'])

user_data['Duration'] = ask_question("How long have you been experiencing this issue?", [
    'Less than a week', '1–2 weeks', '1–3 months', 'More than 3 months'])

user_data['Past Condition'] = ask_question("Have you had any diagnosed skin conditions in the past?", [
    'Yes', 'No', 'Not sure'])

user_data['Using Products'] = ask_question("Are you currently using any skincare or treatment products?", [
    'Yes', 'No', 'Sometimes'])

user_data['Allergies'] = ask_question("Do you have any known allergies to skincare ingredients?", [
    'Yes', 'No', 'Not sure'])

user_data['Sun Exposure'] = ask_question("How often do you get sun exposure?", [
    'Rarely', 'Occasionally', 'Daily, but short', 'Daily and long periods'])

user_data['Exercise'] = ask_question("How often do you engage in physical exercise?", [
    'Rarely or never', '1–2 times a week', '3–4 times a week',
    '5 or more times a week', 'Daily'])

user_data['Sweat'] = ask_question("Do you usually sweat a lot during exercise?", [
    'Yes', 'No', 'Sometimes'])

# Convert to DataFrame
df = pd.DataFrame([user_data])

# Encode using label encoders
for column in df.columns:
    df[column] = label_encoders[column].transform(df[column])

# Predict disease
prediction = model.predict(df)
predicted_disease = target_encoder.inverse_transform(prediction)[0]

# Get confidence score
probabilities = model.predict_proba(df)[0]
confidence = max(probabilities) * 100

# Output
print(f"\n Predicted Disease: {predicted_disease}")
print(f" Confidence Score: {confidence:.2f}%")

# Get and print recommendations
recommendation = get_recommendations(predicted_disease)
print(f"\n Recommendations for {predicted_disease}:")
print(f" Description: {recommendation['description']}")
print(" Products:")
for product in recommendation['products']:
    print(f"  - {product['name']}: {product['description']}")
print(" Diet:")
for diet in recommendation['diet']:
    print(f"  - {diet['name']}: {diet['description']}")
