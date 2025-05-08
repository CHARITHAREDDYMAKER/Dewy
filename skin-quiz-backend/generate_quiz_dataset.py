import pandas as pd
import random

# Define all options
age_groups = ["Under 13", "13–18", "19–30", "31–45", "46–60", "Over 60"]
skin_types = ["Oily", "Dry", "Combination", "Normal", "Sensitive", "Not sure"]
main_issues = ["Acne / Pimples", "Redness / Rashes", "Dry or Flaky Skin", "Dark spots or Hyperpigmentation", "Itching or Irritation", "Other / Not sure"]
durations = ["Less than a week", "1–2 weeks", "1–3 months", "More than 3 months"]
past_conditions = ["Yes", "No", "Not sure"]
using_products = ["Yes", "No", "Sometimes"]
allergies = ["Yes", "No", "Not sure"]
sun_exposure = ["Rarely", "Occasionally", "Daily, but short", "Daily and long periods"]
exercise_freq = ["Rarely or never", "1–2 times a week", "3–4 times a week", "5 or more times a week", "Daily"]
sweating = ["Yes", "No", "Sometimes"]

# Mapping Main Issue to Disease
issue_to_disease = {
    "Acne / Pimples": "Acne",
    "Redness / Rashes": "Rosacea",
    "Dry or Flaky Skin": "Eczema",
    "Dark spots or Hyperpigmentation": "Panu",
    "Itching or Irritation": "Herpes",
    "Other / Not sure": "Unknown"
}

# Generate random data
data = []

for _ in range(5000):  # You can change 5000 to any number you want
    age = random.choice(age_groups)
    skin = random.choice(skin_types)
    issue = random.choice(main_issues)
    duration = random.choice(durations)
    past = random.choice(past_conditions)
    products = random.choice(using_products)
    allergy = random.choice(allergies)
    sun = random.choice(sun_exposure)
    exercise = random.choice(exercise_freq)
    sweat = random.choice(sweating)
    disease = issue_to_disease[issue]
    
    data.append([age, skin, issue, duration, past, products, allergy, sun, exercise, sweat, disease])

# Create DataFrame
columns = ["Age Group", "Skin Type", "Main Issue", "Duration", "Past Condition", "Using Products", "Allergies", "Sun Exposure", "Exercise", "Sweat", "Disease"]
df = pd.DataFrame(data, columns=columns)

# Save as CSV
df.to_csv('skin_quiz_data.csv', index=False)

print("Dataset created successfully: skin_quiz_data.csv")
