import streamlit as st
import numpy as np
import pickle
from nbconvert import PythonExporter
import nbformat
from llm_helper import get_gemini_response

# Function to execute the notebook
def execute_notebook(notebook_path):
    # Load the notebook
    with open(notebook_path) as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Convert notebook to Python code
    exporter = PythonExporter()
    code, _ = exporter.from_notebook_node(notebook_content)

    # Execute the code
    exec(code)

# Run the notebook when the app starts
execute_notebook('Rock_vs_Mine_Prediction.ipynb')

# Load the trained model
with open("rock_vs_mine_model.pkl", "rb") as f:
    model = pickle.load(f)

# Streamlit UI
st.title("Rock vs Mine Prediction")
st.write("Enter 60 SONAR feature values to predict if it's a rock or a mine.")

# Input form
input_data = []
for i in range(60):
    value = st.number_input(f"Feature {i+1}", min_value=0.0, max_value=1.0, step=0.01)
    input_data.append(value)

# Predict button
if st.button("Predict"):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)[0]

    if prediction == 1:
        result = "Mine"
    else:
        result = "Rock"

    st.success(f"Prediction: {result}")
    
    # Get model explanation (replace with your function for explanation)
    prompt = f"Explain why the model predicted '{result}' for the given SONAR feature values."
    explanation = get_gemini_response(prompt)
    st.info(f"AI Explanation:\n{explanation}")
