import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Load your data
df = pd.read_csv('data/healthcare_dataset.csv')

# Encode categorical variables
label_encoders = {}
for column in ['Gender', 'Blood Type', 'Medical Condition', 'Medication', 'Admission Type']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Encode the target variable
y = df['Test Results']
label_encoders['Test Results'] = LabelEncoder()
y = label_encoders['Test Results'].fit_transform(y)

# Split the data
X = df[['Age', 'Gender', 'Blood Type', 'Medical Condition', 'Medication', 'Admission Type']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the XGBoost model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_train, y_train)

def predict_test_result(age, gender, blood_type, medical_condition, medication, admission_type):
    # Prepare the input data
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [label_encoders['Gender'].transform([gender])[0]],
        'Blood Type': [label_encoders['Blood Type'].transform([blood_type])[0]],
        'Medical Condition': [label_encoders['Medical Condition'].transform([medical_condition])[0]],
        'Medication': [label_encoders['Medication'].transform([medication])[0]],
        'Admission Type': [label_encoders['Admission Type'].transform([admission_type])[0]],
    })

    # Make the prediction
    prediction = model.predict(input_data)
    return label_encoders['Test Results'].inverse_transform(prediction)[0]

def show():
    st.title("Test Results Prediction")

    # User input
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    gender = st.selectbox("Gender", options=["Male", "Female"])
    blood_type = st.selectbox("Blood Type", options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    medical_condition = st.selectbox("Medical Condition", options=["Cancer", "Diabetes", "Obesity", "Asthma"])
    medication = st.selectbox("Medication", options=["Paracetamol", "Ibuprofen", "Aspirin", "Penicillin"])
    admission_type = st.selectbox("Admission Type", options=["Urgent", "Emergency", "Elective"])

    if st.button("Predict"):
        result = predict_test_result(age, gender, blood_type, medical_condition, medication, admission_type)
        st.success(f"The predicted Test Result is: **{result}**")

