import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Set up the title and description of the app
st.set_page_config(page_title="Student Marks Predictor", layout="centered")
st.title("🎓 Student Marks Prediction App")
st.write("Enter the details below to predict the student's final Marks based on the trained regression model.")

# Load the trained model
@st.cache_resource
def load_model():
    with open("best_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file 'best_model.pkl' not found. Please upload it to your GitHub repository.")
    st.stop()

# Create input fields based on dataset ranges
st.header("📝 Input Student Metrics")

study_hours = st.slider("Study Hours (per day)", min_value=1.0, max_value=10.0, value=5.5, step=0.1)
attendance = st.slider("Attendance Percentage (%)", min_value=60, max_value=100, value=80, step=1)
sleep_hours = st.slider("Sleep Hours (per night)", min_value=5.0, max_value=9.0, value=7.0, step=0.1)
previous_score = st.slider("Previous Score", min_value=40, max_value=95, value=68, step=1)
internet_hours = st.slider("Internet Hours (per day)", min_value=0.0, max_value=8.0, value=4.0, step=0.1)

# When the user clicks the predict button
if st.button("🔮 Predict Marks"):
    # Organize features into a DataFrame matching the training data feature names and sequence
    input_data = pd.DataFrame([{
        'Study_Hours': study_hours,
        'Attendance_Percentage': attendance,
        'Sleep_Hours': sleep_hours,
        'Previous_Score': previous_score,
        'Internet_Hours': internet_hours
    }])
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    
    # Bound the output between 0 and 100 since exam marks have real physical limits
    final_score = max(0.0, min(100.0, float(prediction)))
    
    # Display the result
    st.success(def_text := f"🎯 Predicted Marks: {final_score:.2f} / 100")
    
    # Provide a simple breakdown context
    st.info(f"Summary of Inputs: Working for {study_hours} hrs with {attendance}% attendance and keeping a prior score baseline of {previous_score}.")